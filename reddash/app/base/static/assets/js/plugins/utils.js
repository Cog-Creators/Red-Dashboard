
/*
 * Project: Utils
 * Description: Utils for Red-Dashboard.
 * Author: ...
 */

$.sendNotification = function(type, message, from="top", align="center", icon="tim-icons icon-bell-55", timer=8000) {
  // types = ["info", "success", "warning", "danger"];
  $.notify(
    {
      icon: icon,
      message: message

    }, 
    {
      type: type,
      timer: timer,
      placement: {
        from: from,
        align: align
      }
    }
  );
};

$.postData = function(data={"data": {}}, url=window.location.href) {
  // submitFunction(**data)
  // .then(response => {
  //   console.log(response);
  // })
  // .catch(error => {
  //   console.error(error);
  // });
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var response = JSON.parse(xhr.responseText);
          if (response && "notifications" in response) {
            response.notifications.forEach(notification => {
                $.sendNotification(notification.type, notification.message);
            });
          resolve(response);
        }
        } catch (error) {
          console.log(error)
          reject(error);
        }
      } else {
        reject(new Error("Request failed with status " + xhr.status));
      }
    };
    xhr.onerror = function() {
      reject(new Error("Network error."));
    };
    xhr.send(JSON.stringify(data));
  });
};

$.showTableRegular = function(element, columns, data) {
  let table = [];
  table.push(`<div class="table-responsive">`);
  table.push(`<table class="table tablesorter " id="simple-table">`);
  table.push(`<thead class=" text-primary">`);
  table.push(`<tr>`);
  for (let c of columns) {
    table.push(`<th>${c}</th>`);
  }
  table.push(`</tr>`);
  table.push(`</thead>`);
  table.push(`<tbody>`);
  for (let e of data) {
    table.push(`<tr>`);
    for (let d of e) {
      table.push(`<td>${d}</td>`);
    }
    table.push(`</tr>`);
  }
  table.push(`</tbody>`);
  table.push(`</table>`);
  table.push(`</div>`);
  element.html(table.join("\n"));
}

$.generateForm = function (element, fields, formID=null, resetForm=true, submitFunction=$.postData, errorFunction=$.sendNotification) {
  // element: the HTML element in which to add the form.
  // fields: an array of objects describing each field of the form. Each object should have the following properties:
  // - name: the name of the property to include in the data sent when the form is submitted.
  // - label: the label text for the field.
  // - type: the type of field to display (optional, default value is "text").
  // - placeholder: the tooltip text to display in the field (optional).
  // - required: a boolean indicating whether the field is required or not (optional, default value is false).
  // - validate: a custom validation function to call on the value of the field (optional).
  // - error: the error message to display if validation fails (optional).
  // formID: the ID of the form to generate.
  // resetForm: reset the form after submit or not.
  // submitFunction: the function to call if the form validation succeeds. This function should take an argument data containing the values of the form fields.
  // errorFunction: the function to call if the form validation fails. This function should take an argument data containing the values of the form fields.
  let form = document.createElement("form");
  element.get(0).appendChild(form);

  for (let field of fields) {
    let label = document.createElement("label");
    label.innerText = field.label;
    form.appendChild(label);
    form.appendChild(document.createElement("br"));

    if (field.type === "select") {
      let select = document.createElement("select");
      select.setAttribute("name", field.name);
      for (let option of field.options) {
        let opt = document.createElement("option");
        opt.setAttribute("value", option.value);
        opt.innerText = option.label;
        select.appendChild(opt);
      }
      select.setAttribute("class", "form-control");
      for (let prop of Object.keys(field)) {
        if (["name", "type", "placeholder", "validate", "error"].includes(prop)) {
          continue;
        }
        select.setAttribute(prop, field[prop]);
      }
      form.appendChild(select);

      if (field.required) {
        select.setAttribute("required", true);
        let asterisk = document.createElement("span");
        asterisk.innerText = " *";
        asterisk.classList.add("required");
        label.appendChild(asterisk);
      }
    } else {
      let input = document.createElement("input");
      input.setAttribute("name", field.name);
      input.setAttribute("type", field.type || "text");
      input.setAttribute("placeholder", field.placeholder || "");
      input.setAttribute("class", "form-control");
      for (let prop of Object.keys(field)) {
        if (["name", "type", "placeholder", "validate", "error"].includes(prop)) {
          continue;
        }
        input.setAttribute(prop, field[prop]);
      }
      form.appendChild(input);

      if (field.required) {
        input.setAttribute("required", true);
        let asterisk = document.createElement("span");
        asterisk.innerText = " *";
        asterisk.classList.add("required");
        label.appendChild(asterisk);
      }
    }

    let error = document.createElement("span");
    error.classList.add("error-message");
    form.appendChild(error);
  }

  let submit = document.createElement("input");
  submit.setAttribute("type", "submit");
  submit.setAttribute("value", "Submit");
  submit.setAttribute("class", "btn");
  form.appendChild(submit);

  // form.addEventListener("invalid", (event) => {
  //   /// event.preventDefault();
  //   let invalidElement = event.target;
  //   let errorMessage = invalidElement.validationMessage;
  //   errorFunction("warning", errorMessage);
  //   /// errorFunction("warning", "Invalid data in the form.");
  // }, true);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let formData = new FormData(form);
    if (validateForm(fields, formData)) {
      let formDataDict = [...formData.entries()].reduce((obj, [key, value]) => {
        obj[key] = value;
        return obj;
      }, {});
      submitFunction({"form_id": formID, "form_data": formDataDict}).then(response => {
        if (response && "errors" in response) {
          let errors = response["errors"];
          for (let fieldName in errors) {
            let error = form.querySelector(`[name="${fieldName}"] + .error-message`);
            if (error) {
              error.innerText = errors[fieldName] + "\n\n";
            }
          }
        }
      }).catch(error => {
          console.error(error);
          $.errorFunction("error", "An error occurred while submitting the form.");
      });
      if (resetForm) {
        form.reset();
      }
    } else {
      errorFunction("warning", "Invalid data in the form.");
    }
  });

  function validateForm(fields, formData) {
    let isValid = true;

    for (let field of fields) {
      let input = formData.get(field.name);
      let error = form.querySelector(`[name="${field.name}"] + .error-message`);

      error.innerText = "";

      if (field.required && !input) {
        error.innerText = "This field is required.";
        isValid = false;
      } else if (field.validate && !field.validate(input)) {
        error.innerText = field.error;
        isValid = false;
      }
    }

    return isValid;
  }
}
