

class GeometryCanvas {
    constructor (width, height, container) {
        this.canvas = document.createElement('canvas')
        container.appendChild(this.canvas)
        this.canvas.setAttribute('width', width)
        this.canvas.setAttribute('height', height)
        this.canvas.style.transform = "scaleY(-1)"

        this.width = width
        this.height = height
        this.context = this.canvas.getContext('2d')
    }

    drawAxis (startX, startY, endX, endY, highlightX=0, highlightY=0, color_context={}) {
        let stroke = color_context.stroke ? color_context.stroke : "#ddd"
        let axis_stroke = color_context.axis_stroke ? color_context.axis_stroke : "#aaa"

        let stepX = this.width  / (endX - startX + 2)
        let stepY = this.height / (endY - startY + 2)
        this.sizeX = (endX - startX + 2)
        this.sizeY = (endY - startY + 2)

        this.stepX = stepX
        this.stepY = stepY

        let posX = stepX
        for (let x = startX; x <= endX; x ++) {
            this.context.strokeStyle = x == highlightX ? axis_stroke : stroke
            if (x == highlightX) this.axisX = posX
            
            this.context.beginPath()
            this.context.moveTo(posX, 0)
            this.context.lineTo(posX, this.height)
            this.context.stroke()

            posX += stepX
        }

        let posY = stepY
        for (let y = startY; y <= endY; y ++) {
            this.context.strokeStyle = y == highlightY ? axis_stroke : stroke
            if (y == highlightY) this.axisY = posY
            
            this.context.beginPath()
            this.context.moveTo(0, posY)
            this.context.lineTo(this.width, posY)
            this.context.stroke()

            posY += stepY
        }
    }

    drawLine (a, b, c, color="#aa0000") {
        let centerX = this.axisX
        let centerY = this.axisY - c / b * this.stepY

        // Normal vectors (-b, a) and (b, -a)
        let left = this.width * -b + centerX
        let right = this.width * b + centerX

        let bottom = this.height * a + centerY
        let top = this.height * -a + centerY

        if (b == 0) {
            left = centerX - c / a * this.stepX;
            right = left;
            bottom = 0
            top = this.height;
        }

        this.context.strokeStyle = color
        this.context.beginPath()
        this.context.moveTo(left, bottom)
        this.context.lineTo(right, top)
        this.context.stroke()
    }

    drawSegment(x0, y0, x1, y1, color="#00ee00") {
        x0 = x0 * this.stepX + this.axisX
        x1 = x1 * this.stepX + this.axisX
        y0 = y0 * this.stepY + this.axisY
        y1 = y1 * this.stepY + this.axisY

        this.context.strokeStyle = color
        this.context.beginPath()
        this.context.moveTo(x0, y0)
        this.context.lineTo(x1, y1)
        this.context.stroke()
    }
}

