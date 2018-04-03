----- Prevent association of a Heroic Deed with a Villian -----
create or replace trigger Check_HeroDisposition
before insert on HeroDisaster
for each row
declare
    V_Disposition varchar2(15);
begin
    select Disposition
    into V_Disposition
    from SuperPerson
    where SuperPerson.SuperID = :new.HeroID;
    
    if V_Disposition != 'GOOD' then
        raise_application_error(-20001, 'Tried to put a villian in the HeroDisaster table');
    end if;
end;
/

----- Prevent association of a Villianous Deed with a Hero -----
create or replace trigger Check_VillianDisposition
before insert on VillianDisaster
for each row
declare
    V_Disposition varchar2(15);
begin
    select Disposition
    into V_Disposition
    from SuperPerson
    where SuperPerson.SuperID = :new.VillianID;
    
    if V_Disposition != 'EVIL' then
        raise_application_error(-20001, 'Tried to put a hero in the VillianDisaster table');
    end if;
end;
/