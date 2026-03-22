from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ------------------ DATA ------------------

movies = [
    {"id": 1, "title": "Leo", "genre": "Action", "language": "Tamil", "duration_mins": 160, "ticket_price": 200, "seats_available": 50},
    {"id": 2, "title": "Jailer", "genre": "Action", "language": "Tamil", "duration_mins": 150, "ticket_price": 180, "seats_available": 40},
    {"id": 3, "title": "KGF", "genre": "Action", "language": "Kannada", "duration_mins": 155, "ticket_price": 220, "seats_available": 30},
    {"id": 4, "title": "RRR", "genre": "Drama", "language": "Telugu", "duration_mins": 170, "ticket_price": 250, "seats_available": 60},
    {"id": 5, "title": "Drishyam", "genre": "Thriller", "language": "Hindi", "duration_mins": 140, "ticket_price": 150, "seats_available": 45},
    {"id": 6, "title": "Bhool Bhulaiyaa", "genre": "Comedy", "language": "Hindi", "duration_mins": 130, "ticket_price": 160, "seats_available": 35}
]

bookings = []
holds = []
booking_counter = 1
hold_counter = 1

# ------------------ MODELS ------------------

class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)
    phone: str = Field(..., min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

class NewMovie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)

class SeatHold(BaseModel):
    customer_name: str
    movie_id: int
    seats: int

# ------------------ HELPERS ------------------

def find_movie(movie_id):
    for m in movies:
        if m["id"] == movie_id:
            return m
    return None

def calculate_ticket_cost(base_price, seats, seat_type, promo_code=""):
    if seat_type == "premium":
        price = base_price * 1.5
    elif seat_type == "recliner":
        price = base_price * 2
    else:
        price = base_price

    original = price * seats

    discount = 0
    if promo_code == "SAVE10":
        discount = original * 0.1
    elif promo_code == "SAVE20":
        discount = original * 0.2

    return {
        "original_cost": original,
        "final_cost": original - discount
    }

def filter_movies_logic(genre, language, max_price, min_seats):
    result = movies
    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]
    if max_price:
        result = [m for m in result if m["ticket_price"] <= max_price]
    if min_seats:
        result = [m for m in result if m["seats_available"] >= min_seats]
    return result

# ------------------ DAY 1 ------------------

@app.get("/")
def home():
    return {"message": "Welcome to CineStar Booking"}

@app.get("/movies")
def get_movies():
    return {
        "total_movies": len(movies),
        "total_seats_available": sum(m["seats_available"] for m in movies),
        "movies": movies
    }

@app.get("/movies/summary")
def summary():
    return {
        "total_movies": len(movies),
        "most_expensive": max(m["ticket_price"] for m in movies),
        "cheapest": min(m["ticket_price"] for m in movies),
        "total_seats": sum(m["seats_available"] for m in movies),
        "genre_count": {g: len([m for m in movies if m["genre"] == g]) for g in set(m["genre"] for m in movies)}
    }

# ------------------ FILTER + SEARCH (FIXED ORDER) ------------------

@app.get("/movies/filter")
def filter_movies(
    genre: Optional[str] = None,
    language: Optional[str] = None,
    max_price: Optional[str] = None,
    min_seats: Optional[str] = None
):
    try:
        max_price = int(max_price) if max_price else None
    except:
        raise HTTPException(400, "max_price must be number")

    try:
        min_seats = int(min_seats) if min_seats else None
    except:
        raise HTTPException(400, "min_seats must be number")

    return filter_movies_logic(genre, language, max_price, min_seats)

@app.get("/movies/search")
def search_movies(keyword: str):
    result = [
        m for m in movies
        if keyword.lower() in m["title"].lower()
        or keyword.lower() in m["genre"].lower()
        or keyword.lower() in m["language"].lower()
    ]

    if not result:
        return {"message": "No results found"}

    return {
        "total_found": len(result),
        "data": result
    }

@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):
    if sort_by not in ["ticket_price", "title", "duration_mins", "seats_available"]:
        raise HTTPException(400, "Invalid sort field")

    return sorted(movies, key=lambda x: x[sort_by], reverse=(order == "desc"))

@app.get("/movies/page")
def paginate(page: int = 1, limit: int = 3):
    total = len(movies)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "data": movies[(page - 1) * limit: page * limit]
    }

@app.get("/movies/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3,
    genre: Optional[str] = None,
    language: Optional[str] = None
):
    result = movies

    if keyword:
        result = [m for m in result if keyword.lower() in m["title"].lower()]

    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]

    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    total = len(result)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "data": result[(page - 1) * limit: page * limit]
    }

# ❗ ALWAYS LAST
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    m = find_movie(movie_id)
    if not m:
        raise HTTPException(404, "Movie not found")
    return m

@app.get("/bookings")
def get_bookings():
    return {
        "total": len(bookings),
        "total_revenue": sum(b.get("final_cost", 0) for b in bookings),
        "bookings": bookings
    }

# ------------------ BOOKINGS ------------------

@app.post("/bookings", status_code=201)
def create_booking(data: BookingRequest):
    global booking_counter

    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if data.seats > movie["seats_available"]:
        raise HTTPException(400, "Not enough seats")

    cost = calculate_ticket_cost(movie["ticket_price"], data.seats, data.seat_type, data.promo_code)

    movie["seats_available"] -= data.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": data.customer_name,
        "movie_title": movie["title"],
        "seats": data.seats,
        "seat_type": data.seat_type,
        "original_cost": cost["original_cost"],
        "final_cost": cost["final_cost"]
    }

    bookings.append(booking)
    booking_counter += 1
    return booking

# ------------------ CRUD ------------------

@app.post("/movies", status_code=201)
def add_movie(data: NewMovie):
    if any(m["title"].lower() == data.title.lower() for m in movies):
        raise HTTPException(400, "Duplicate movie")

    new = data.dict()
    new["id"] = len(movies) + 1
    movies.append(new)
    return new

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, ticket_price: Optional[int] = None, seats_available: Optional[int] = None):
    m = find_movie(movie_id)
    if not m:
        raise HTTPException(404, "Not found")

    if ticket_price is not None:
        m["ticket_price"] = ticket_price
    if seats_available is not None:
        m["seats_available"] = seats_available

    return m

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    m = find_movie(movie_id)
    if not m:
        raise HTTPException(404, "Not found")

    if any(b["movie_title"] == m["title"] for b in bookings):
        raise HTTPException(400, "Movie has bookings")

    movies.remove(m)
    return {"message": "Deleted"}

# ------------------ WORKFLOW ------------------

@app.post("/seat-hold", status_code=201)
def hold_seat(data: SeatHold):
    global hold_counter

    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if data.seats > movie["seats_available"]:
        raise HTTPException(400, "Not enough seats")

    movie["seats_available"] -= data.seats

    hold = {
        "hold_id": hold_counter,
        "movie_id": data.movie_id,
        "seats": data.seats
    }

    holds.append(hold)
    hold_counter += 1
    return hold

@app.get("/seat-hold")
def get_holds():
    return holds

@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    for h in holds:
        if h["hold_id"] == hold_id:
            booking = {
                "booking_id": len(bookings) + 1,
                "movie_id": h["movie_id"],
                "seats": h["seats"]
            }
            bookings.append(booking)
            holds.remove(h)
            return booking
    raise HTTPException(404, "Hold not found")

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    for h in holds:
        if h["hold_id"] == hold_id:
            movie = find_movie(h["movie_id"])
            movie["seats_available"] += h["seats"]
            holds.remove(h)
            return {"message": "Released"}
    raise HTTPException(404, "Hold not found")

# ------------------ BOOKINGS SEARCH ------------------

@app.get("/bookings/search")
def search_bookings(customer_name: str):
    result = [
        b for b in bookings
        if customer_name.lower() in b["customer_name"].lower()
    ]

    if not result:
        return {"message": "No bookings found"}

    return {
        "total_found": len(result),
        "data": result
    }


# ------------------ BOOKINGS SORT ------------------

@app.get("/bookings/sort")
def sort_bookings(sort_by: str = "final_cost", order: str = "asc"):
    if sort_by not in ["final_cost", "seats"]:
        raise HTTPException(400, "Invalid sort field")

    return sorted(bookings, key=lambda x: x[sort_by], reverse=(order == "desc"))


# ------------------ BOOKINGS PAGINATION ------------------

@app.get("/bookings/page")
def paginate_bookings(page: int = 1, limit: int = 2):
    total = len(bookings)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "data": bookings[(page - 1) * limit: page * limit]
    }