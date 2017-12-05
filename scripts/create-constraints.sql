-- Add Foreign Key Constraints to all Tables

-------- Super Person --------
alter table SuperPerson
add constraint FK_HideoutID foreign key(HideoutID)
    references Hideout(HideoutID)
    on delete set null;

alter table SuperPerson
add constraint FK_NemesisID foreign key(NemesisID)
    references SuperPerson(SuperID)
    on delete set null;

-------- Sidekick --------
alter table Sidekick
add constraint FK_MentorID foreign key(MentorID)
    references SuperPerson(SuperID)
    on delete cascade;

-------- Power --------
alter table Powers
add constraint FK_PowersSuperID foreign key(SuperID)
    references SuperPerson(SuperID)
    on delete cascade;

-------- Origin Story --------
alter table OriginStory
add constraint FK_OriginStorySuperID foreign key(SuperID)
    references SuperPerson(SuperID)
    on delete cascade;

-------- Equipment --------
alter table Equipment
add constraint FK_OwnerID foreign key(OwnerID)
    references SuperPerson(SuperID)
    on delete cascade;

-------- Disasters --------
alter table HeroDisaster
add constraint FK_HeroID foreign key(HeroID)
    references SuperPerson(SuperID)
    on delete cascade;

alter table HeroDisaster
add constraint FK_HeroEventID foreign key(EventID)
    references Disaster(EventID)
    on delete cascade;

alter table VillianDisaster
add constraint FK_VillianID foreign key(VillianID)
    references SuperPerson(SuperID)
    on delete cascade;

alter table VillianDisaster
add constraint FK_VillianEventID foreign key(EventID)
    references Disaster(EventID)
    on delete cascade;
