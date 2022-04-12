/**
 * Project Graphic Calculator
 * 
 * The goal is to create an inequality or equality project to view math curves
 * 
 * @author MrThimote
 * @source https://github.com/MrThimote/js-graphic-calculator/
 * @version https://github.com/MrThimote/js-graphic-calculator/commit/57e6214bed994e796973b4d1880c0c4640fe3fb8
 */

/**
 * Canvas
 */
 class GeometryCanvas {
    constructor (width, height, container=document.body) {
        this.width  = width;
        this.height = height;

        this.canvas  = document.createElement("canvas")
        this.canvas.setAttribute("width",  width)
        this.canvas.setAttribute("height", height)

        this.context = this.canvas.getContext("2d")
        container.appendChild(this.canvas)
    }

    generateAxis(sX, eX, sY, eY, hX=0, hY=0, c0="#dddddd", c1="#888") {
        this.start = [sX, sY];
        this.end   = [eX, eY];

        this.length       = [eX - sX, eY - sY]
        this.white_length = [this.length[0] + 2, this.length[1] + 2]

        this.steps = [ this.width / this.white_length[0], this.height / this.white_length[1] ]
        
        let offX = this.steps[0]
        for (let x = this.start[0]; x <= this.end[0]; x++) {
            this.context.strokeStyle = x == hX ? c1 : c0;
            if (x == hX) this.axisX = offX;

            this.context.beginPath()
            this.context.moveTo(offX, 0)
            this.context.lineTo(offX, this.height)
            this.context.stroke()

            offX += this.steps[0]
        }

        let offY = this.height - this.steps[1]
        for (let y = this.start[1]; y <= this.end[1]; y++) {
            this.context.strokeStyle = y == hY ? c1 : c0;
            if (y == hY) this.axisY = offY;

            this.context.beginPath()
            this.context.moveTo(0,          offY)
            this.context.lineTo(this.width, offY)
            this.context.stroke()

            offY -= this.steps[1]
        }
    }

    mapX (x) {
        return this.axisX + this.steps[0] * x
    }
    mapY (x) {
        return this.axisY - this.steps[1] * x
    }

    unmapX (x) {
        return (x - this.axisX) / this.steps[0]
    }
    unmapY (x) {
        return - (x - this.axisY) / this.steps[1]
    }

    setStroke (color) {
        this.context.strokeStyle = color
        this.context.fillStyle = color
        this.context
    }

    getArrays (sx=undefined, ex=undefined) {
        if (sx == undefined)
            sx = [0, 0]
        else
            sx = [this.mapX(sx[0]), this.mapY(sx[1])]

        if (ex == undefined)
            ex = [this.width, this.height]
        else
            ex = [this.mapX(ex[0]), this.mapY(ex[1])]
        
        if (sx[0] > ex[0]) {
            let c = ex[0]
            ex[0] = sx[0]
            sx[0] = c;
        }
        if (sx[1] > ex[1]) {
            let c = ex[1]
            ex[1] = sx[1]
            sx[1] = c;
        }

        return { sx, ex }
    }

    drawEqual (f0, f1, sx=undefined, ex=undefined) {
        ({ sx, ex } = this.getArrays(sx, ex))

        let lastX = undefined
        let lastY = undefined

        for (let x = sx[0]; x < ex[0]; x ++) {
            for (let y = sx[1]; y < ex[1]; y ++) {
                let rx = this.unmapX(x)
                let ry = this.unmapY(y)
                let ex = this.unmapX(x + 1)
                let ey = this.unmapY(y + 1)

                let val = f0(rx, ry) - f1(rx, ry)
                let next = f0(ex, ry) - f1(ex, ry)
                let next2 = f0(rx, ey) - f1(rx, ey)
                let next3 = f0(ex, ey) - f1(ex, ey)

                let root_array = [0, val, next, next2, next3]
                root_array = root_array.sort()

                if (root_array.indexOf(0) != 0 && root_array.indexOf(0) != root_array.length - 1) {
                    this.context.fillRect(x, y, 2, 2)
                }
            }
        }
    }

    drawInEqual (f0, f1, sx=undefined, ex=undefined) {
        ({ sx, ex } = this.getArrays(sx, ex))

        let lastX = undefined
        let lastY = undefined

        for (let x = sx[0]; x < ex[0]; x ++) {
            for (let y = sx[1]; y < ex[1]; y ++) {
                let rx = this.unmapX(x)
                let ry = this.unmapY(y)

                let val = f0(rx, ry) - f1(rx, ry)
                let is_root = val < 0

                if (is_root) {
                    this.context.fillRect(x, y, 1, 1)
                }
            }
        }
    }
}

