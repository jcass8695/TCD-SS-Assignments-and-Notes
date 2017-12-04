drop table SuperPerson;
create table SuperPerson (
    SuperID number(9) not null,
    Alias varchar2(20) not null,
    TrueFName varchar2(15),
    TrueSName varchar2(15),
    Universe varchar2(15) constraint CK_Universe check(Universe in ('DC', 'Marvel')),
    Disposition varchar2(4) constraint CK_Disposition check(Disposition in ('GOOD', 'EVIL', null)),
    HideoutID number(9),
    NemesisID number(9),
    constraint PK_SuperPerson primary key(SuperID)
);

drop table Sidekick;
create table Sidekick(
    SidekickID number(9) not null,
    SidekickName varchar(15) not null,
    MentorID number(9) not null,
    constraint PK_Sidekick primary key(SidekickID)
);

drop table Powers;
create table Powers(
    SuperID number(9) not null,
    Power varchar2(15) not null,
    constraint PK_Powers primary key(SuperID, Power)
);

drop table OriginStory;
create table OriginStory(
    StoryID number(9) not null,
    StoryDesc varchar2(500),
    SuperID number(9) not null,
    constraint PK_OriginStory primary key(StoryID)
);

drop table Hideout;
create table Hideout(
    HideoutID number(9) not null,
    HideoutName varchar(20),
    AddressCity varchar(15),
    constraint PK_Hideout primary key(HideoutID)
);

drop table Equipment;
create table Equipment(
    SerialNum number(9) not null,
    EquipmentName varchar2(15) not null,
    Cost number(9),
    OwnerID number(9) not NULL,
    constraint PK_Equipment primary key(SerialNum)
);

drop table Disaster;
create table Disaster(
    EventID number(9) not null,
    DamageCost number(9),
    NumCivCasualties number(9),
    EventDate date,
    constraint PK_Disaster primary key(EventID)
);

drop table HeroDisaster;
create table HeroDisaster(
    EventID number(9) not null,
    HeroID number(9) not null,
    constraint PK_HeroDisaster primary key(EventID, HeroID)
);

drop table VillianDisaster;
create table VillianDisaster(
    EventID number(9) not null,
    VillianID number(9) not null,
    constraint PK_VillianDisaster primary key(EventID, VillianID)
);