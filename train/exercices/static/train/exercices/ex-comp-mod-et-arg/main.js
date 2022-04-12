
function pgcd(a, b) {
    while (b != 0) {
        let t = b;
        b = a % b;
        a = t;
    }

    return a;
}

EXERCICE_PLAYER.register ( 'comp-mod-et-arg', function generator ( html ) {
    let mod = Math.floor(Math.random() * 3) % 3 + 2
    let args = []
    for (let idx = -5; idx <= 6; idx ++) {
        args.push(Math.PI / 6 * idx)
    }

    let idx = Math.floor(Math.random() * args.length) % args.length
    let arg = args[idx]

    let a = mod * (Math.cos(arg))
    let b = mod * (Math.sin(arg))

    return { mod, arg, a, b, idx, html }

}, function show_exercice(exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("hidden")
    
    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))
    
    canvas.generateAxis(-5, 5, -5, 5)
    let point_func = (x, y) => { return Math.pow(x - exercice.a, 2) + Math.pow(y - exercice.b, 2) }
    let null_func = (x, y) => 1 / 125
    canvas.setStroke("#1111ff")
    canvas.drawInEqual(point_func, null_func)
}, function show_solution (exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("").replace("<%mod%>", exercice.mod).replace("<%idx%>", exercice.idx - 5)

    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))

    canvas.generateAxis(-5, 5, -5, 5)

    let point_func = (x, y) => { return Math.pow(x - exercice.a, 2) + Math.pow(y - exercice.b, 2) }
    let null_func = (x, y) => 1 / 125
    canvas.setStroke("#1111ff")
    canvas.drawInEqual(point_func, null_func)

    let dist_func = (x, y) => Math.pow(x, 2) + Math.pow(y, 2)
    let radius_func = (x, y) => Math.pow(exercice.a, 2) + Math.pow(exercice.b, 2)

    canvas.setStroke("#1111ff22")
    canvas.drawEqual(radius_func, dist_func)
} )
