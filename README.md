# Python Hexagonal Architecture Template

A clean and structured template for building Python applications following the Hexagonal Architecture (also known as Ports and Adapters) pattern and Domain-Driven Design (DDD) principles.

## 🏗️ Project Structure

The project is organized into the following key directories:

### 📂 `app`

Contains the core of your framework.

### 📂 `src`

Contains the core of your application and the domain logic.

#### 📂 `bounded_contexts`

Contains the bounded contexts of your application.

#### 📂 `modules`

Contains the modules of your application.


### 📂 `tests`

Contains the tests of your application.

## 🎯 Purpose

This template provides a starting point for building applications using Hexagonal Architecture, which offers:

- Clear separation of concerns
- Domain-centric design
- Framework independence
- Highly testable code
- Maintainable and scalable structure

## 🏛️ Architectural Overview

The project follows these key principles:

1. **Domain Layer** (`domain/`)
   - Contains the business logic
   - Pure Python with no external dependencies
   - Defines interfaces (ports) for external operations

2. **Application Layer** (`application/`)
   - Orchestrates the flow of data and implements use cases
   - Coordinates between the domain and infrastructure layers

3. **Infrastructure Layer** (`infrastructure/`)
   - Implements adapters for external services
   - Contains framework-specific code
   - Implements the interfaces defined in the domain layer

## 🚀 Getting Started

1. Clone this repository:
```bash
git clone https://github.com/your-username/python-hexagonal-architecture
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

## 📝 Usage

1. Create your bounded contexts under `src/`
2. Define your domain model in the `domain/` layer
3. Implement use cases in the `application/` layer
4. Add adapters in the `infrastructure/` layer
5. Write tests following the same structure in `tests/`

## 🧪 Testing

Run tests using:
```bash
pytest
```

## 📦 Project Dependencies

- **Development**: See `requirements/dev.txt`
- **Testing**: See `requirements/test.txt`
- **Production**: See `requirements/prod.txt`
- **Common**: See `requirements/common.txt`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Additional Resources

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)