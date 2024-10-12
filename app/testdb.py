import datetime
from app import app, db
from app.database import *

with app.app_context():
	print("initialising test database...")
	#Assumes you initialise an admin with createadmin and env file, but will create an admin user here.
	AddUser("admin@admin.com", "Admin", "Admin", "password", "admin")
	#Admin creates unit:
	unit1 = AddUnit("CITS3000", "Computing 101", "Sem1",  datetime(2024, 8, 12).date(), datetime(2024, 11, 10).date(), "Lab|Workshop", "Morning|Afternoon", 1, 1, 1, "nomark|suggest")
	#Assign facilitators to unit
	AddUser("22224444@uwa.edu.au", "Facilitator1", "Lastname", "facilitator1", "facilitator")
	AddUser("33335555@uwa.edu.au", "Facilitator2", "Lastname", "facilitator2", "facilitator")
	AddUser("44446666@uwa.edu.au", "Coordinator1", "Coordinate", "coordinate", "coordinator")
	#Add units to users
	AddUnitToCoordinator("admin@admin.com", unit1)
	AddUnitToFacilitator("admin@admin.com", unit1)
	AddUnitToFacilitator("22224444@uwa.edu.au", unit1)
	AddUnitToFacilitator("33335555@uwa.edu.au", unit1)
	AddUnitToCoordinator("44446666@uwa.edu.au", unit1)
	AddUnitToFacilitator("44446666@uwa.edu.au", unit1)
	#Add sessions to unit
	AddSession(unit1, "Lab", "Morning", datetime.now())
	AddSession(unit1, "Workshop", "Morning", datetime.now())
	#Add students to unit/sessions
	AddStudent(55557777, "Alice", "Alicelast", "Ms", "Alice", unit1, "no")
	AddStudent(66668888, "Robert", "Boblast", "Mr", "Bob", unit1, "no")
	AddStudent(77777777, "Cathy", "Cathylast(con)", "Ms", "Cathy", unit1, "yes")
	AddStudent(88888888, "David", "Davidlast", "Mr", "David", unit1, "no")
	AddStudent(99999999, "Eve", "Evelast(con)", "Ms", "Eve", unit1, "yes")
	AddStudent(11111111, "Frank", "Franklast", "Mr", "Frank", unit1, "no")
	print("successful!")
