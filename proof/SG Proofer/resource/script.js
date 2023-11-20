console.log("hello")
var get_style = function(value) {
    return cssStyles.getPropertyValue(value).trim();
}

var set_style = function(element, property, value) {
    return element.style.setProperty(property, value);
}

var changeFont = function(font){
    affect = document.getElementById("font-proof")
    console.log(font.value)
    console.log(affect)
    affect.style.fontFamily = font.value;
}

function slider_get(slider_id, output_id, affect_style, fvar_tag, fvar_unit="") {
    // Init
    var slider = document.getElementById(slider_id);
    var output = document.getElementById(output_id);
    var affect = document.getElementById(affect_style)

    output.innerHTML = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.innerHTML = this.value;
        document.documentElement.style.setProperty(`--vf-${fvar_tag}`, `${this.value}${fvar_unit}`)
        affect.style.setProperty('font-size', 'var(--vf-size)');
        affect.style.setProperty('font-variation-settings','"YOPQ" var(--vf-YOPQ), "slnt" var(--vf-slnt), "wdth" var(--vf-wdth), "wght" var(--vf-wght)');
    }
}

slider_get("fsize", "fsize-val", "proof_input", "size","px")
slider_get("YOPQ", "YOPQ-val", "proof_input", "YOPQ")
slider_get("slant", "slnt-val", "proof_input", "slnt")
slider_get("width", "wdth-val", "proof_input", "wdth")
slider_get("weight", "weight-val", "proof_input", "wght")
