# Overview

This is a **Quotation Webhook Handler** application built with Flask that serves as a webhook endpoint for receiving and managing quotation data. The application provides a web dashboard for viewing quotations, an API documentation page, and handles webhook requests with proper validation. It's designed to receive quotation data from external systems and display them in a user-friendly interface with search and filtering capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates for server-side rendering
- **CSS Framework**: Bootstrap 5 with dark theme for consistent UI styling
- **JavaScript**: Vanilla JavaScript for client-side interactions including auto-refresh functionality and search enhancements
- **Responsive Design**: Mobile-first approach using Bootstrap's responsive grid system

## Backend Architecture
- **Web Framework**: Flask as the primary web framework
- **Data Storage**: In-memory storage using Python lists (temporary storage solution)
- **Request Handling**: RESTful API design with proper HTTP status codes and JSON responses
- **Middleware**: ProxyFix middleware for handling reverse proxy headers
- **Validation**: Custom validation functions for quotation data structure and required fields

## Data Model
- **Quotation Structure**: JSON objects with required fields (id, customer_name, items, total_amount)
- **Item Structure**: Nested objects within quotations containing name, quantity, and unit_price
- **Validation Layer**: Comprehensive validation for data types and required fields

## Application Structure
- **Route Organization**: Separate routes for dashboard, API documentation, and webhook endpoints
- **Error Handling**: Structured error responses with descriptive messages
- **Logging**: Comprehensive logging system using Python's logging module
- **Session Management**: Flask sessions with configurable secret key

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: UI framework for responsive design and dark theme
- **Font Awesome 6.4.0**: Icon library for consistent iconography throughout the application

## Python Packages
- **Flask**: Core web framework for handling HTTP requests and responses
- **Werkzeug**: WSGI utilities including ProxyFix middleware for deployment behind reverse proxies

## Development Tools
- **Replit CDN**: Bootstrap theme specifically designed for dark mode compatibility

## Notes
- Currently uses in-memory storage which is suitable for development but would need to be replaced with a persistent database solution for production use
- No authentication system currently implemented
- Webhook endpoint accepts POST requests with JSON payloads containing quotation data