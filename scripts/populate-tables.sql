----- SuperPerson -----
insert into SuperPerson values(1, 'Batman', 'Bruce', 'Wayne', 'DC', 'GOOD', 1, 2);
insert into SuperPerson values(2, 'The Joker', null, null, 'DC', 'EVIL', null, 1);
insert into SuperPerson values(3, 'SpiderMan', 'Peter', 'Parker', 'Marvel', 'GOOD', 2, 4);
insert into SuperPerson values(4, 'The Hulk', 'Bruce', 'Banner', 'Marvel', 'GOOD', null, 7);
insert into SuperPerson values(5, 'Iron Man', 'Tony', 'Stark', 'Marvel', 'GOOD', 3, null);
insert into SuperPerson values(6, 'The Flash', 'Barry', 'Allen', 'DC', 'GOOD', 6, 7);
insert into SuperPerson values(7, 'The Reverse Flash', 'Eobard', 'Thawne', 'DC', 'EVIL', null, 6);
insert into SuperPerson values(8, 'SuperMan', 'Clark', 'Kent', 'DC', 'GOOD', 5, null);
insert into SuperPerson values(9, 'Green Goblin', 'Harry', 'Osbourne', 'Marvel', 'EVIL', 3, 3);
insert into SuperPerson values(10, 'Two Face', 'Harvey', 'Dent', 'DC', 'EVIL', 1, null);
insert into SuperPerson values(11, 'Dr Doom', 'Victor', 'Von Doom', 'Marvel', 'EVIL', null, null);

----- Sidekick -----
insert into Sidekick values(1, 'Robyn', 1);
insert into Sidekick values(2, 'Rick Jones', 4);
insert into Sidekick values(3, 'Harley Quinn', 2);
insert into Sidekick values(4, 'War Machine', 5);
insert into Sidekick values(5, 'Krypto', 7);

----- Powers ------
insert into Powers values(1, 'Wealth');
insert into Powers values(1, 'Genius');
insert into Powers values(3, 'Strength');
insert into Powers values(3 ,'Wall Climbing');
insert into Powers values(4 , 'Strength');
insert into Powers values(4, 'Genius');
insert into Powers values(5, 'Wealth');
insert into Powers values(5, 'Genius');
insert into Powers values(6, 'Speed');

------ Origin Story -----
insert into OriginStory values(
    1, 
    'As a young boy, Bruce Wayne was horrified and traumatized when 
    he watched his parents, the physician Dr. Thomas Wayne and his wife Martha, murdered with a gun 
    by a mugger named Joe Chill.', 
    1
);
insert into OriginStory values(
    2,
    'Though a number of backstories have been given, a definitive one has not yet been established 
    for the Joker. An unreliable narrator, the character is uncertain of who he was before and how 
    he became the Joker',
    2
);
insert into OriginStory values(
    3, 
    'One evening Parker attended a public exhibition demonstrating the safe handling of nuclear 
    laboratory waste materials sponcored by the General Techtronics Corporation. 
    During the demonstration, a small Common House Spider happened to be in the path of a particle 
    accelerators beam and was massively irradiated. The stricken spider fell on to Parkers hand, 
    broke his skin with its fangs, and died.', 
    3
);
insert into OriginStory values(
    4,
    'Supervising the trial of an experimental gamma bomb that he designed for the U.S. Defense 
    Department at a nuclear research facility in New Mexico, Bruce selflessly rushed to the rescue 
    of an Rick Jones who had wandered onto the testing field as the countdown ticked 
    inexorably toward zero. Bruce was struck full-force by the bomb blast. He survived, but was 
    irradiated by the deadly gamma energy.', 
    4
);
insert into OriginStory values(
    5, 
    'Superman is born Kal-El on the alien planet Krypton. His parents, Jor-El and Lara become 
    aware of Kryptons impending destruction and Jor-El constructs a spacecraft to carry 
    Kal-El to Earth. During Kryptons last moments, Jor-El places Kal-El in the spacecraft. 
    Jor-El and Lara die as the spacecraft barely escapes Kryptons fate.',
    7
);

----- Hideout -----
insert into Hideout values(1, 'The Bat Cave', 'Gotham');
insert into Hideout values(2, 'Aunt Mays House', 'New York City');
insert into Hideout values(3, 'Osbourne Manor', 'New York City');
insert into Hideout values(4, 'Stark Mansion', 'Malibu');
insert into Hideout values(5, 'Xaviers School', 'Westchester');
insert into Hideout values(6, 'Flashs Apartment', 'Central City');
insert into Hideout values(7, 'Hulkbuster Base', 'New Mexico');
insert into Hideout values(8, 'Fortress of Solidtude', null)

----- Equipment -----
insert into Equipment values(123456789, 'Bat-a-Rang', 500, 1);
insert into Equipment values(234567891, 'Same Sided Coin', 1, 10);
insert into Equipment values(345678912, 'Blunt Knife', 2.50, 2);
insert into Equipment values(456789123, 'Iron Man Suit', 7000000, 5);
insert into Equipment values(567891234, 'BatMobile', 9000000, 1);

----- Disaster -----
insert into Disaster values(1, 10000, 10, '08-JUN-1995');
insert into Disaster values(2, 500000, 0, '23-DEC-1992');
insert into Disaster values(3, 32452, 3, '12-DEC-1990');
insert into Disaster values(4, 78324, 21, '30-APR-1999');
insert into Disaster values(5, 7821634, 0,'06-FEB-1997');

----- Hero Disaster -----
insert into HeroDisaster values(1, 1);
insert into HeroDisaster values(2, 5);
insert into HeroDisaster values(3, 6);
insert into HeroDisaster values(4, 3);
insert into HeroDisaster values(5, 1);

----- Villian Disaster -----
insert into VillianDisaster values(1, 2);
insert into VillianDisaster values(2, 11);
insert into VillianDisaster values(3, 7);
insert into VillianDisaster values(4, 9);
insert into VillianDisaster values(5, 10);