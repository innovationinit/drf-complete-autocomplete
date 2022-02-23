import os
import sys

test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def run_tests():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testapp.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    sys.exit(execute_from_command_line(['manage.py', 'test']))


if __name__ == '__main__':
    run_tests()
