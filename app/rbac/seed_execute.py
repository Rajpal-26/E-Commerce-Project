from app import create_app
from app.rbac.seed import seed_rbac   

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        seed_rbac()
        print("RBAC seeding completed successfully!")