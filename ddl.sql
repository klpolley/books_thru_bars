BEGIN TRANSACTION;

create table if not exists genre(
    genreId serial primary key,
    name varchar not null unique,
    color varchar,
    label varchar,

    unique(color, label)
);

create table if not exists book(
    bookId serial primary key,
    title varchar not null unique,
    genreId integer not null,

    foreign key (genreId) references genre(genreId)
);

create table if not exists copy(
    copyId serial primary key,
    bookId integer,
    logged date,
    sent date,

    check (sent >= logged),

    foreign key (bookId) references book(bookId)
);

create table if not exists storage(
    locationId serial primary key,
    name varchar not null,
    capacity int
);

create table if not exists book_location(
    copyId integer,
    locationId integer,

    primary key(copyId, locationId),

    foreign key (copyId) references copy(copyId),
    foreign key (locationId) references storage(locationId)
);

create table if not exists author(
    authorId serial primary key,
    name varchar not null
);

create table if not exists editor(
    editorId serial primary key,
    name varchar not null
);

create table if not exists written_by(
    bookId integer,
    authorId integer,

    primary key (bookId, authorId),

    foreign key (bookId) references book(bookId),
    foreign key (authorId) references author(authorId)
);

create table if not exists edited_by(
    bookId integer,
    editorId integer,

    primary key (bookId, editorId),

    foreign key (bookId) references book(bookId),
    foreign key (editorId) references editor(editorId)
);

create table if not exists state(
    stateId serial primary key,
    name varchar not null,
    abbreviation varchar(2) not null
);

create table if not exists facility(
    facilityId serial primary key,
    name varchar not null,
    address varchar,
    stateId integer,

    unique (name, stateId),

    foreign key (stateId) references state(stateId)
);

create table if not exists package(
    packageId serial primary key,
    facilityId integer,
    dateSent date,

    foreign key (facilityId) references facility(facilityId)
);

create table if not exists restriction(
    restrictionId serial primary key,
    description varchar
);

create table if not exists facility_restriction(
    facilityId integer,
    restrictionId integer,

    primary key (facilityId, restrictionId),

    foreign key (facilityId) references facility(facilityId),
    foreign key (restrictionId) references restriction(restrictionId)
);

create table if not exists state_restriction(
    stateId integer,
    restrictionId integer,

    primary key (stateId, restrictionId),

    foreign key (stateId) references state(stateId),
    foreign key (restrictionId) references restriction(restrictionId)
);

COMMIT;

