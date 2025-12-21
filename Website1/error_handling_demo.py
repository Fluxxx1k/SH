#!/usr/bin/env python3
"""
Demo script showing how to use the error handling functionality
"""

from flask import Flask, render_template_string
import sys
import os

# Add the current directory to the path so we can import from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import render_error_page, handle_game_error, handle_database_error

def demo_error_functions():
    """Demonstrate the error handling functions"""
    print("=== Secret Hitler Error Handling Demo ===\n")
    
    # Create a minimal Flask app for testing
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    with app.app_context():
        print("1. Testing 404 error page:")
        try:
            result = render_error_page(
                error_code=404,
                error_message="Игра не найдена",
                error_description="Запрошенная игра не существует или была удалена.",
                error_comment="Возможно, игра уже завершилась или вы ввели неправильное имя.",
                suggestion="Попробуйте вернуться в лобби и выбрать другую игру."
            )
            print("✓ 404 error page generated successfully")
            print(f"  Response length: {len(str(result))} characters")
        except Exception as e:
            print(f"✗ Error generating 404 page: {e}")
        
        print("\n2. Testing 500 error page:")
        try:
            result = render_error_page(
                error_code=500,
                error_message="Ошибка сервера",
                error_description="Произошла ошибка при обработке игровых данных.",
                error_comment="Возможно, проблема с базой данных или логикой игры.",
                suggestion="Попробуйте обновить страницу. Если ошибка повторяется, обратитесь к администратору.",
                debug_info="Database connection failed at line 42 in game_logic.py"
            )
            print("✓ 500 error page generated successfully")
            print(f"  Response length: {len(str(result))} characters")
        except Exception as e:
            print(f"✗ Error generating 500 page: {e}")
        
        print("\n3. Testing game-specific error:")
        try:
            result = handle_game_error("Недостаточно игроков для начала игры")
            print("✓ Game error handled successfully")
            print(f"  Response length: {len(str(result[0]))} characters")
        except Exception as e:
            print(f"✗ Error handling game error: {e}")
        
        print("\n4. Testing database error:")
        try:
            result = handle_database_error("Connection timeout to database")
            print("✓ Database error handled successfully")
            print(f"  Response length: {len(str(result[0]))} characters")
        except Exception as e:
            print(f"✗ Error handling database error: {e}")

def show_usage_examples():
    """Show usage examples for developers"""
    print("\n=== Usage Examples for Developers ===\n")
    
    print("1. Basic error handling in routes:")
    print("""
    @app.route('/game/<game_name>')
    def game(game_name):
        try:
            game_data = find_game_data(game_name)
            if not game_data:
                return render_error_page(
                    error_code=404,
                    error_message="Игра не найдена",
                    error_description=f"Игра '{game_name}' не существует."
                ), 404
            
            # ... rest of the code ...
            
        except Exception as e:
            return handle_database_error(str(e))
    """)
    
    print("\n2. Using game-specific error handler:")
    print("""
    if player_count < MIN_PLAYERS:
        return handle_game_error(
            f"Недостаточно игроков. Необходимо минимум {MIN_PLAYERS} игроков."
        )
    """)
    
    print("\n3. Manual error route usage:")
    print("""
    # In browser:
    http://localhost:20050/error?code=404&message=Custom+error&description=Details
    
    # Parameters:
    # code - HTTP error code (default: 500)
    # message - Short error message
    # description - Detailed description
    # comment - Additional comment
    # suggestion - What user can do
    """)

def main():
    """Main demo function"""
    demo_error_functions()
    show_usage_examples()
    
    print("\n=== Demo Completed ===")
    print("\nTo test the error pages in browser:")
    print("1. Start the server: python app.py")
    print("2. Visit: http://localhost:20050/nonexistent-page (404)")
    print("3. Visit: http://localhost:20050/error?code=500&message=Test (500)")
    print("4. Visit: http://localhost:20050/lobby (401/redirect when not logged in)")
    print("\nOr run the test script: python test_errors.py")

if __name__ == "__main__":
    main()