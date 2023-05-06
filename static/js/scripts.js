/*
let itemQty, itemQtyValue;

let addButtonElements = document.querySelectorAll('[id^="add-btn"]');
let removeButtonElements = document.querySelectorAll('[id^="remove-btn"]');

// Loop over the selected elements and add a click event listener to each one
addButtonElements.forEach((buttonElement) => {
    buttonElement.addEventListener('click', () => {
        // Handle the click event here
        //console.log(`Button with id "${buttonElement.id}" was clicked.`);
        let id = buttonElement.id.slice(7);
        addToCart(id);
    });
});

removeButtonElements.forEach((buttonElement) => {
    buttonElement.addEventListener('click', () => {
        // Handle the click event here
        //console.log(`Button with id "${buttonElement.id}" was clicked.`);
        let id = buttonElement.id.slice(10);
        removeFromCart(id);
    });
});

function addToCart(id) {
    let itemQty = document.getElementById('qty' + id);
    //console.log(id);
    let itemQtyValue = parseInt(itemQty.innerHTML);
    itemQty.innerHTML = itemQtyValue + 1;
}

function removeFromCart(id) {
    let itemQty = document.getElementById('qty' + id);
    //console.log(id);
    let itemQtyValue = parseInt(itemQty.innerHTML);
    if (itemQtyValue > 0) {
        itemQty.innerHTML = itemQtyValue - 1;
    }
}

document.getElementById("openmodal").addEventListener("click", () => {
    document.getElementById("my-modal").classList.remove('modal');
});
document.getElementById("closemodal").addEventListener("click", () => {
    document.getElementById("my-modal").classList.add('modal');
});*/

function toggle() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}


