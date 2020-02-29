var fs = require("fs");

function readFromInitialFile(path, callback) {
    fs.open("model.txt", 'r', function (err, fd) {
        if (err) {
            return console.error(err);
        }
        var buffr = new Buffer(1024);
        fs.read(fd, buffr, 0, buffr.length, 0, function (err, bytes) {
            if (err) throw err;
            if (bytes > 0) {
                console.log(buffr.slice(0, bytes).toString());
            }
        });
        fs.close(fd, function (err) {
            if (err)
                throw err;
        })
    });
    callback(path, " Ce faceti in aceasta minunata seara?", copy)
}

function append(path, message, callback) {
    fs.open(path, "a+",function (err, fd) {
        if(err) {
            return console.error(err);
        }
        fs.writeFile(fd, message, function (err){
            if(err) {
                return console.error(err);
            }
        });
        fs.fdatasync(fd, function(err){
            if(err) {
                return console.error(err);
            }
        });
        fs.close(fd, function (err) {
            if (err)
                throw err;
        })
    });
    callback(path, "altmodel.txt", deleteFile)
}

function copy(source, destination, callback) {
    fs.copyFile(source, destination, function(err) {
        if(err) {
            return console.error(err);
        }
    });
    callback(source);
}

function deleteFile(path) {
    fs.unlink(path, function(err) {
        if (err) {
            return console.error(err);
        }
    });
}

readFromInitialFile("model.txt", append);

