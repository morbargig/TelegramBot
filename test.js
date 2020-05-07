class APromise {
    constructor(Fn) {
        this.value = null;
        Fn(resolved => { this.value = resolved; });
        this.callbacks = [];
        Fn(resolved => {
            this.value = resolved;

            this.callbacks.forEach(cb => {
                cb(this.value);
            });
        });
    }
    then(fn) {
        // fn(this.value);
        this.callbacks.push(fn);
        return this;
    }
}

function myFun() {
    return new APromise(resolve => {
        setTimeout(() => { resolve ( 'Hello') ; }, 2000);
    });
}

// const log = v => { v != null ? console.log(v) : null; };
const log = v => {  console.log(v) ; };

// myFun().then(log).then(log);