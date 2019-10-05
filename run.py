from app import db
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        script_namespace = __import__('scripts.' + script_name)
        script_module = getattr(script_namespace, script_name)
        script_fn = getattr(script_module, script_name)
        script_fn()
    else:
        db.create_tables()
        db.create_district_data()
        db.print_district_completeness()
        db.print_example_queries()
