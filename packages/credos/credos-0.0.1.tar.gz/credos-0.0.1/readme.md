# Credos: Conflict-free Replicated Document Store

This is a work-in-progress package and not yet functional. (Popping a squat in
the namespace real quick.)

The goal of this project is to create a replicated storage package using CRDTs
and sqlite3 via the [crdts](https://pypi.org/project/crdts) and
[sqloquent](https://pypi.org/project/sqloquent) packages, respectively. Using
CRDTs, any number of updates can be made to a local replica without the need for
any consensus or commitment mechanism -- so long as all updates (state deltas)
are eventually applied by all replicas, all replicas will converge to the same
state. Additionally, authorization will use
[tapescript](https://pypi.org/project/tapescript), and serialization will
probably use [packify](https://pypi.org/project/packify) in early dev stages.

Ever want to have a replicated database with sub millisecond reads and writes
that did not cost a fortune in dedicated database hosting costs? This should
allow for applications to be built using an entirely new database model that
requires only a few bootstrap nodes to connect application servers for blazingly
bonkers fasterest databaseness.

## Goals

The following are what will comprise the base system:

- Base models: LWWRegister/LWWMap + sqloquent
- Replicated key-value/document store
- Synchronization worker
- Auth system for sync protocol messages

## Stretch Goals

The following are ideas I am contemplating once the base system is done:

- Sharded key-value/document store using Highest Random Weight/Rendezvous Hashing
- Record-level ACL

## ISC License

Copyright (c) 2024 Jonathan Voss (k98kurz)

Permission to use, copy, modify, and/or distribute this software
for any purpose with or without fee is hereby granted, provided
that the above copyleft notice and this permission notice appear in
all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
