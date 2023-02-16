class ap {
    valueoffset
    timeoffset

    constructor() {
        this.valueoffset = this.recoverylimit()
        this.timeoffset = 0
    }

    recoverylimit() {
        return 100;
    }

    recoveryperseconds() {
        return 1 / 500;
    }

    overflow() {
        return undefined;
    }

    getepoch() {
        return new Date().getTime() / 1000;
    }

    getvalueontime(targettime) {
        if (this.timeoffset == 0) {
            return this.valueoffset;
        }
        ///if (this.timeoffset > 0) {
        let rawvalue = this.valueoffset + Math.floor((targettime - this.timeoffset) * this.recoveryperseconds());
        if (rawvalue >= this.recoverylimit()) {
            rawvalue = this.valueoffset = this.recoverylimit()
            this.timeoffset = 0
        }
        ///}
        return rawvalue;
    }

    getcurrent() {
        return this.getvalueontime(this.getepoch());
    }

    consume(ap) {
        let newvalue = this.getcurrent() - ap;
        if (newvalue >= this.overflow()) {
            newvalue = this.overflow();
        }
        this.valueoffset = newvalue;
        this.timeoffset = this.recoverylimit() <= newvalue ? 0 : this.getepoch();
        return this.getcurrent()
    }

    recovery(ap) {
        return this.consume(-ap)
    }

}

module.exports = ap;