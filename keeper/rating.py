# app/routers/rating.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from .database import get_db_connection
from .models import RatingCreate, ShopItem, PurchaseRequest, RedCoinsUpdate

router = APIRouter(prefix="", tags=["Rating & Shop"])

# BLUE RATING
@router.get("/employees/{employee_id}/blue-rating-history/")
def get_blue_rating_history(employee_id: int, period: Optional[str] = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            query = """
                SELECT delta, reason, created_at FROM blue_rating
                WHERE employee_id = %s
                ORDER BY created_at ASC
            """
            
            cur.execute(query, (employee_id, ))
            history = cur.fetchall()
            
            return {
                "total_bcoins": sum(i['delta'] for i in history),
                "history": history
            }

@router.patch("/employees/{employee_id}/blue-rating/")
def update_blue_rating(employee_id: int, increment_data: RatingCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
                        
            cur.execute("""
                INSERT INTO blue_rating (employee_id, delta, reason)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (employee_id, increment_data.delta, increment_data.reason))
            
            new_rating = cur.fetchone()
            
            return new_rating
        
# RED RATING
@router.patch("/employees/{employee_id}/red-rating/")
def update_red_rating(employee_id: int, increment_data: RatingCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Employee not found")
                        
            cur.execute("""
                INSERT INTO red_rating (employee_id, delta, reason)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (employee_id, increment_data.delta, increment_data.reason))
            
            new_rating = cur.fetchone()
            
            return new_rating
        
@router.get("/employees/{employee_id}/red-rating-history/")
def get_red_rating_history(employee_id: int, period: Optional[str] = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM employees WHERE id = %s", (employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            query = """
                SELECT delta, reason, created_at FROM red_rating
                WHERE employee_id = %s
                ORDER BY created_at ASC
            """
            
            cur.execute(query, (employee_id, ))
            history = cur.fetchall()
            
            return {
                "total_rcoins": sum(i['delta'] for i in history),
                "history": history
            }

@router.get("/shop/", response_model=List[ShopItem])
def get_shop_items():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM shop_items WHERE is_available = TRUE ORDER BY price_rcoins")
            items = cur.fetchall()
            return items

@router.post("/shop/{item_id}/purchase/")
def purchase_shop_item(item_id: int, purchase_data: PurchaseRequest):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, rcoins FROM employees WHERE id = %s", (purchase_data.employee_id,))
            employee = cur.fetchone()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            
            cur.execute("SELECT * FROM shop_items WHERE id = %s AND is_available = TRUE", (item_id,))
            item = cur.fetchone()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            
            total_price = item['price_rcoins'] * purchase_data.quantity
            if employee['rcoins'] < total_price:
                raise HTTPException(status_code=400, detail="Not enough rcoins")
            
            cur.execute("INSERT INTO red_rating (delta, reason, employee_id) VALUES (%s, %s, %s)", (-total_price, "Купил " + item['name'], purchase_data.employee_id))
            
            cur.execute("""
                INSERT INTO purchases (employee_id, shop_item_id, quantity)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (purchase_data.employee_id, item_id, purchase_data.quantity))
            
            purchase = cur.fetchone()
            conn.commit()
            
            return {
                "message": "Purchase successful",
                "purchase_id": purchase['id'],
                "item_name": item['name'],
                "quantity": purchase_data.quantity,
                "total_cost": total_price,
                "remaining_rcoins": employee['rcoins'] - total_price
            }
        
@router.get("/leaderboard/blue-coins", response_model=List[dict])
def get_blue_coins_leaderboard(limit: int = 10):
    """Получить лидерборд по Blue Coins"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.position,
                    COALESCE(SUM(br.delta), 0) as total_blue_coins,
                    COUNT(br.id) as transactions_count
                FROM employees e
                LEFT JOIN blue_rating br ON e.id = br.employee_id
                GROUP BY e.id, e.name, e.position
                ORDER BY total_blue_coins DESC
                LIMIT %s
            """, (limit,))
            
            leaderboard = cur.fetchall()
            return leaderboard