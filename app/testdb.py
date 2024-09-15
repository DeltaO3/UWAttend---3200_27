import datetime
from app import app, db
from app.database import *

with app.app_context():
	print("initialising test database...")
	#Assumes you initialise an admin with createadmin and env file, but will create an admin user here.
	AddUser(12345678, "Admin", "Admin", "password", 1)
	#Admin creates unit:
	unit1 = AddUnit("CITS3000", "Unit", "Sem1", 1, datetime(2024, 8, 12).date(), datetime(2024, 11, 10).date(), "Lab|Workshop", "Morning|Afternoon", 1, 1, 1, "nomark|suggest")
	#Assign facilitators to unit
	AddUser(22224444, "Facilitator1", "Lastname", "facilitator1", 3)
	AddUser(33335555, "Facilitator2", "Lastname", "facilitator2", 3)
	AddUser(44446666, "Coordinator1", "Coordinate", "coordinate", 2)
	#Add units to users
	AddUnitToCoordinator(12345678, unit1)
	AddUnitToFacilitator(22224444, unit1)
	AddUnitToFacilitator(33335555, unit1)
	AddUnitToCoordinator(44446666, unit1)
	#Add sessions to unit
	AddSession(unit1, "Lab", "Morning", datetime.now())
	AddSession(unit1, "Workshop", "Morning", datetime.now())
	#Add students to unit/sessions
	AddStudent(55557777, "Alice", "Alicelast", "Ms", "Alice", unit1, 0)
	AddStudent(66668888, "Robert", "Boblast", "Mr", "Bob", unit1, 0)
	AddStudent(77777777, "Cathy", "Cathylast", "Ms", "Cathy", unit1, 1)
	print("successful!")