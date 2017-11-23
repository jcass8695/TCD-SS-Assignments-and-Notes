# CS4400-Internet-Applications-Distributed-File-System
Assignment3: A RESTful CRUD distributed file system

File system features:
* File Server: Simple server that simply dishes out requested files. Super dumb and _stateless_
* Directory Server: Routes client opens, reads, writes and deletes of files to the specific File Server holding that file
* Locking Server: Ensures concurrency control on alterations to files
