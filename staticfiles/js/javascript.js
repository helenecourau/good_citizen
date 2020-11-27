function cleanPage() {
    list = document.getElementsByTagName("input");
    for (let elt of list){
        elt.checked = false;
    }
}

function checkIfSend(questions, checkedBoxes) {
	let toSend = true;
	for (let question of questions) {
        let isChecked = false
        for (let checkedBoxe of checkedBoxes) {
            if (question['id']===checkedBoxe['name']) {
                isChecked = true
            }
        }
        if (isChecked===false) {
            let alert = document.createElement('p');
            alert.textContent = "Vous devez choisir au moins une réponse !"
            alert.style.color = "red"
            question.append(alert)
            toSend = false
        }
    }
    return toSend
}

function disableButton() {
	button = document.getElementById("submit");
    button.disabled = true;
}

function createData(checkedBoxes) {
	let checkboxesChecked = [];
    let controlList = [];
    for (let checkedBoxe of checkedBoxes) {
        valueList = [];
        let key = Number(checkedBoxe['name']);
        let value = Number(checkedBoxe['value'])
        if (controlList.includes(key) == true) {
            checkboxesChecked.find(obj => {
                if (obj.key === key) {
                    obj.value.push(value);
                }
            })
        }
        else {
            valueList.push(value)
            let answer = {
                key: key,
                value: valueList,
            };
            controlList.push(key)
            checkboxesChecked.push(answer)
        }
    }
    return checkboxesChecked
}

function displayResult(json) {
	let total_result = json["total_result"]
    let title = document.getElementsByTagName("h2")[0];
    let result_p = document.createElement('p');
    if (json["final_result"] === true) {
        result_p.textContent = "Vous avez " + total_result + " bonne(s) réponse(s). Bravo, vous avez réussi ce quizz !"
    } else {
        result_p.textContent = "Vous avez " + total_result + " bonne(s) réponse(s). Vous n'avez pas réussi ce quizz, réessayez plus tard."
    }
    title.append(result_p)
}

function goodAnswer(json) {
	for (let [key, values] of Object.entries(json["right_answers"])) {
        for (let value of values) {
            let node = document.getElementById(key+value)
            node.className = 'right'
            node.insertAdjacentHTML('afterbegin', "<i class=\"fas fa-check\" color=green></i>&nbsp;");
        }
    }
}

function badAnswer(json, checkboxesChecked) {
	for (let [key, values] of Object.entries(checkboxesChecked)) {
        for (let value of values.value) {
            let node = document.getElementById(values.key.toString()+value.toString())
            if (node.className != "right") {
                node.insertAdjacentHTML('afterbegin', "<i class=\"fa fa-times\" color=red></i>&nbsp;");
            }
        }
    }
}

function main(checkedBoxes, url) {
	disableButton ();       
    let checkboxesChecked = createData(checkedBoxes);
    let serializedData = JSON.stringify(checkboxesChecked);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        url: url,
        data: {"answer_id":serializedData},
        success: function (json) {
            displayResult(json);
            goodAnswer(json);
            badAnswer(json, checkboxesChecked);
        },
    })
}