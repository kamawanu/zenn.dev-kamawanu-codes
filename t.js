///
const ap = require("./oreap.js") ;
/////console.log(ap);

class apv extends ap {
    timeshift = 0
    getepoch() {
        return super.getepoch() + this.timeshift
    }
}

const apo = new apv();
console.log(apo.getcurrent());
console.log(apo.consume(50))
apo.timeshift = 500
console.log(apo.getcurrent())
apo.timeshift = 500*50
console.log(apo.getcurrent())
apo.timeshift = 500*60
console.log(apo.getcurrent())
console.log(apo.recovery(50))
console.log(apo.recovery(50))
console.log(apo.recovery(50))
