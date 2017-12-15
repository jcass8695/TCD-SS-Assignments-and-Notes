# CS4400-Internet-Applications-Distributed-File-System
Assignment3: A RESTful CRUD distributed NFS

File system features:
* File Server: Simple server that simply dishes out requested file text. Super dumb and _stateless_
* Directory Server: Routes client opens, reads, writes and deletes of files to the specific File Server holding that file
* Locking Server: Ensures concurrency control on alterations to files
* Caching: For faster reads and writes and reduced network traffic
* A Client API for CRUD operations


## How does it work?
### Directory Server
Whenever a client wants to make a CRUD operation, the Directory Server (DS) is always asked for the location of the file, the location being the IP and Port of the File Server (FS) hosting the file. The DS maintains two local MongoDB databases. The files db contains the locations of every file that is in circulation, as well as the ID of the machine they're located on. The machines db translates that machine ID to an IP and a Port.

### Locking Server
On a write operation from the client, the client must get the file location from the DS and then ask the Locking Server (LS) for exclusive access to the file until the write is complete. The LS maintains no information on which files or machines exist, it simply maintains a MongoDB database of '_entities_' that are locked and not locked.

### Caching
Files can be cached for quicker read and write times. On the initial read of a new file, the files text and file age will be pulled from the FS over the network. The file text and age will be entered into the clients local MongoDB database, simulating a cached copy. All reads are now redirected to this cached copy

On a write, if the file being written to is cached, the client API will request the remote file age from the DS. The cache is invalidated if the local copy is older than the remote copy. In this situation, the client is requested to do a manual merge and the new changes are attempted to be written again.
