------ View that hides the Super's real names and their hideouts -----
create view SuperPrivacy as
select SuperPerson.SuperID, SuperPerson.Alias, SuperPerson.Universe, 
SuperPerson.Disposition, SuperPerson.NemesisID
from SuperPerson
/
------ View that shows who owns what -----
create view OwnerToEquipment as
select SuperPerson.Alias, Equipment.EquipmentName
from SuperPerson
inner join Equipment
on SuperPerson.SuperID = Equipment.OwnerID
/