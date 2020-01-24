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

create table if not exists event(
    eventId serial primary key,
    type varchar,
    date date
);

create table if not exists copy(
    copyId serial primary key,
    bookId integer,
    logged integer,
    sent integer,

    foreign key (bookId) references book(bookId),
    foreign key (logged) references event(eventId),
    foreign key (sent) references event(eventId)
);

create function log_book() returns trigger as $$
    BEGIN
    
        if (select type from new inner join event on logged = eventId where eventId = new.logged) != "Logging"
        then raise exception 'must log book at mailing event';
        end if;

        if (select type from new inner join event on sent = eventId where eventId = new.sent) != "Mailing"
        then raise exception 'must send book at mailing event';
        end if;

        if (select date from new inner join event on sent = eventId where eventId = new.sent) < 
            (select date from new inner join event on logged = eventId where eventId = new.logged)
        then raise exception 'must send after logging';
        end if;

        return new;
    END;
$$ LANGUAGE plpgsql;

create trigger log_book before insert or update on copy
    for each row execute procedure log_book();

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

