let criteriaField = document.getElementById("date-search-criteria")
let criteria = criteriaField === null ? null : criteriaField.value
let searchFieldWrapper = document.getElementById("search-field-wrapper");


let labelElement1 = `<label class="small mb-1" id="search-label1" for="input-search-date">{label1}</label>`;
let labelElement2 = `<label class="small mb-1" id="search-label2" for="input-search-date">{label2}</label>`;

let searchField1 = `
<div class="input-group col" id="date-picker1" data-target-input="nearest">
    <input type="{criteria}" class="form-control" name="input-search-date1"/>
</div>`;

let searchField2 = `
<div class="input-group col" id="date-picker2" data-target-input="nearest">
    <input type="{criteria}" class="form-control" name="input-search-date2"/>
</div>`;

let yearSearchField = `
<div class="input-group col" id="date-picker1" data-target-input="nearest">
    <select name="input-search-date1" id="date-picker1" class="form-control">
        <option value="2019" selected>2019</option>
        <option value="2020">2020</option>
    </select>
</div>`;

function changeCriteria(criteria, label1, label2) {
    var searchFieldString = "";

    
    if(criteria === "year"){
        searchFieldWrapper.innerHTML = yearSearchField;
    } else{
        searchFieldString += (labelElement1.replace("{label1}", label1) + searchField1.replace("{criteria}", criteria));
        searchFieldString += (labelElement2.replace("{label2}", label2) + searchField2.replace("{criteria}", criteria));
        searchFieldWrapper.innerHTML = searchFieldString;
    }
}