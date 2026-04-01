"""Quick verification test for the two fixes."""
from pathlib import Path
import importlib.util

BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples" / "book-app-project"


def _load_module(module_name: str, file_name: str):
    module_path = SAMPLES_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


book_app = _load_module("book_app", "book_app.py")
books = _load_module("books", "books.py")

handle_add = book_app.handle_add
main = book_app.main
BookCollection = books.BookCollection

def test_empty_string_validation():
    """Test that empty strings via CLI are properly rejected."""
    collection = BookCollection()
    
    # Capture output
    outputs = []
    def mock_print(msg):
        outputs.append(msg)
    
    # Test 1: Empty title string should be rejected
    print("Test 1: Empty title string")
    handle_add(collection, title="", author="Author", year="2020", print_func=mock_print)
    
    # Check that it was rejected
    if any("cannot be empty" in str(o).lower() for o in outputs):
        print("✓ Empty title correctly rejected")
    else:
        print("✗ ISSUE: Empty title NOT rejected!")
        print(f"  Outputs: {outputs}")
    
    outputs.clear()
    
    # Test 2: Empty author string should be rejected
    print("\nTest 2: Empty author string")
    handle_add(collection, title="Title", author="", year="2020", print_func=mock_print)
    
    if any("cannot be empty" in str(o).lower() for o in outputs):
        print("✓ Empty author correctly rejected")
    else:
        print("✗ ISSUE: Empty author NOT rejected!")
        print(f"  Outputs: {outputs}")
    
    # Test 3: Verify books were not added
    print(f"\nTest 3: Collection should have 0 books")
    books = collection.list_books()
    if len(books) == 0:
        print(f"✓ Collection has {len(books)} books (correct)")
    else:
        print(f"✗ ISSUE: Collection has {len(books)} books (should be 0)!")

def test_exception_handling():
    """Test that main() has proper exception handling."""
    print("\n\nTest 4: Exception handling in main()")
    
    # Test with a command that will work
    result = main(["list"], collection=BookCollection())
    print(f"✓ main() returns exit code: {result}")
    
    # Test that main has try-except around handler dispatch
    import inspect
    source = inspect.getsource(main)
    if "try:" in source and "handler(collection, args)" in source:
        print("✓ main() has try-except around handler dispatch")
    else:
        print("✗ ISSUE: main() may not have proper exception handling!")

if __name__ == "__main__":
    test_empty_string_validation()
    test_exception_handling()
