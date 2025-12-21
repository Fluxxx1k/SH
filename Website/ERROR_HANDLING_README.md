# Secret Hitler - Error Handling System

## Overview

The error handling system provides comprehensive error pages with user-friendly messages, proper HTTP status codes, and visual feedback. It includes protection against missing parameters and various error scenarios.

## Features

### 1. Comprehensive Error Pages
- **404 Not Found**: When page doesn't exist
- **500 Internal Server Error**: For server errors with debug info in development
- **403 Forbidden**: For access denied scenarios
- **401 Unauthorized**: For authentication required scenarios
- **400 Bad Request**: For invalid request data
- **405 Method Not Allowed**: For incorrect HTTP methods

### 2. Error Template Components
Each error page includes:
- **Error Code**: HTTP status code
- **Error Message**: Brief description
- **Error Description**: Detailed explanation
- **Error Comment**: Additional context
- **Suggestion**: What user can do
- **Visual Icons**: Emoji and SVG icons for different error types
- **Action Buttons**: Links to home, lobby, login, or back
- **Auto-redirect**: Automatic redirect to homepage after 30 seconds

### 3. Protection Against Missing Parameters
The system handles cases where:
- Error code is missing (defaults to 500)
- Error message is missing (shows generic message)
- Description/comment/suggestion are missing (shows helpful defaults)
- Template rendering fails (fallback to simple HTML)

## Usage

### Basic Error Handling in Routes

```python
from app import render_error_page, handle_game_error, handle_database_error

@app.route('/game/<game_name>')
def game(game_name):
    try:
        game_data = find_game_data(game_name)
        if not game_data:
            return render_error_page(
                error_code=404,
                error_message="Игра не найдена",
                error_description=f"Игра '{game_name}' не существует.",
                error_comment="Возможно, игра уже завершилась.",
                suggestion="Попробуйте вернуться в лобби и выбрать другую игру."
            ), 404
        
        # ... rest of the code ...
        
    except DatabaseError as e:
        return handle_database_error(str(e))
    except GameLogicError as e:
        return handle_game_error(str(e))
```

### Manual Error Route

Access the error page manually with parameters:

```
http://localhost:20050/error?code=404&message=Custom+error&description=Details&comment=Comment&suggestion=Try+this
```

**Parameters:**
- `code` - HTTP error code (default: 500)
- `message` - Short error message
- `description` - Detailed description
- `comment` - Additional comment
- `suggestion` - What user can do

### Error Handler Functions

```python
# Game-specific errors
def handle_game_error(error_message, error_code=400):
    return render_error_page(
        error_code=error_code,
        error_message="Ошибка в игре",
        error_description=error_message,
        error_comment="Проверьте правильность действий в игре.",
        suggestion="Попробуйте вернуться в лобби и начать заново."
    ), error_code

# Database errors
def handle_database_error(error_message):
    return render_error_page(
        error_code=500,
        error_message="Ошибка базы данных",
        error_description="Произошла ошибка при работе с базой данных.",
        error_comment="Возможно, проблема с соединением или данными.",
        suggestion="Попробуйте обновить страницу. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=error_message if app.debug else None
    ), 500
```

## Visual Design

### Error Icons
- **404**: Detective emoji 🕵️ + SVG detective icon
- **500**: Warning emoji ⚠️ + SVG warning icon
- **403**: Lock emoji 🔒 + SVG shield icon
- **401**: Lock emoji 🔐 + SVG lock icon
- **Generic**: Cross emoji ❌ + SVG generic icon

### Styling
- Consistent with main site design (dark theme, red accents)
- Responsive design for mobile devices
- Animated pulsing icons
- Color-coded error types
- Professional typography

## Testing

### Test Script
Run the test script to verify error handling:

```bash
-deleted-
```

### Manual Testing
Visit these URLs to test different errors:

```bash
# 404 error
http://localhost:20050/nonexistent-page

# Custom error with parameters
http://localhost:20050/error?code=404&message=Test+message&description=Test+description

# Protected route (should redirect or show 401)
http://localhost:20050/lobby
```

### Demo Script
Run the demo script to see error handling in action:

```
-deleted-
```

## Files Created

1. **`templates/error.html`** - Main error template
2. **`static/error.css`** - Error page styles
3. **`static/error-icons.svg`** - SVG icons for different error types
4. **`test_errors.py`** - Test script for error handling
5. **`error_handling_demo.py`** - Demo script showing usage
6. **Updated `app.py`** - Added error handlers and functions

## Error Page Structure

```html
<div class="error-container">
  <div class="error-icon">
    <!-- Emoji + SVG icon based on error code -->
  </div>
  
  <div class="error-content">
    <h1 class="error-title">Error [code]</h1>
    <p class="error-message">[error_message]</p>
    
    <div class="error-description">
      <p>[error_description]</p>
    </div>
    
    <div class="error-comment">
      <p><strong>Комментарий:</strong> [error_comment]</p>
    </div>
    
    <div class="error-suggestion">
      <h3>Что можно сделать:</h3>
      <p>[suggestion]</p>
    </div>
  </div>
  
  <div class="error-actions">
    <a href="/" class="btn btn-primary">На главную</a>
    <a href="/lobby" class="btn btn-secondary">В лобби</a>
    <button onclick="history.back()" class="btn btn-info">Назад</button>
  </div>
  
  <!-- Debug info in development mode -->
  <div class="error-debug" *ngIf="debug_mode">
    <h3>Техническая информация:</h3>
    <pre>[debug_info]</pre>
  </div>
</div>
```

## Best Practices

1. **Always provide meaningful error messages**
2. **Use appropriate HTTP status codes**
3. **Include helpful suggestions for users**
4. **Add debug information in development mode**
5. **Test error scenarios thoroughly**
6. **Use consistent error handling throughout the application**
7. **Provide fallback options (home, lobby, back)**
8. **Make error pages visually consistent with the main site**

## Security Considerations

- Debug information is only shown in development mode
- Error messages don't expose sensitive system information
- User input in error parameters is properly escaped
- Error pages maintain session security

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design for mobile devices
- SVG icons work in all modern browsers
- Fallback to emoji icons if SVG fails