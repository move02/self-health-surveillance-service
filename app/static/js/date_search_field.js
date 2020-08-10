let criteriaField = document.getElementById("date-search-criteria")
let criteria = criteriaField === null ? null : criteriaField.value
let searchFieldWrapper = document.getElementById("search-field-wrapper");


let labelElement1 = `<label class="small mb-1" id="search-label1" for="input-search-date">{label1}</label>`;
let labelElement2 = `<label class="small mb-1" id="search-label2" for="input-search-date">{label2}</label>`;

let searchField1 = `
<div class="input-group col" id="datetimepicker" data-target-input="nearest">
    <input type="text" class="form-control datetimepicker-input" name="input-search-date" data-target="#datetimepicker"/>
    <div class="input-group-append" data-target="#datetimepicker" data-toggle="datetimepicker">
        <div class="input-group-text"><i class="fa fa-calendar"></i></div>
    </div>
</div>`;

let searchField2 = `
<label class="small mb-1" id="search-label2" for="input-search-date"></label>
<div class="input-group col" id="datetimepicker2" data-target-input="nearest">
    <input type="text" class="form-control datetimepicker-input" name="input-search-date" data-target="#datetimepicker2"/>
    <div class="input-group-append" data-target="#datetimepicker2" data-toggle="datetimepicker">
        <div class="input-group-text"><i class="fa fa-calendar"></i></div>
    </div>
</div>`;

let yearSearchField = `
<div class="input-group year col" id="datetimepicker" data-target-input="nearest">
    <select name="input-date" id="datetimepicker" class="form-control">
        <option value="2019" selected>2019</option>
        <option value="2020">2020</option>
    </select>
</div>`;

function changeCriteria(criteria, label1, label2) {
    var searchFieldString = "";
    if(label1 !== null && label1 !== undefined){
        labelElement1 = labelElement1.replace("{label1}", label1);
        searchFieldString += (labelElement1 + searchField1);
    } else {
        searchFieldString += searchField1;
    }
    if(label2 !== null && label2 !== undefined){
        labelElement2 = labelElement2.replace("{label2}", label2);
        searchFieldString += (labelElement2 + searchField2);
    } else {
        searchFieldString += searchField2;
    }
    
    if(criteria === "day" || criteria === null){
        searchFieldWrapper.innerHTML = searchFieldString;
        $('#datetimepicker').datetimepicker({ format: "YYYY/MM/DD", Default: true });
        $('#datetimepicker2').datetimepicker({ format: "YYYY/MM/DD", Default: true });
    } else if(criteria === "month"){
        searchFieldWrapper.innerHTML = searchFieldString;
        $('#datetimepicker').datetimepicker({ format: "YYYY/MM", Default: true });
        $('#datetimepicker2').datetimepicker({ format: "YYYY/MM", Default: true });
    } else if(criteria === "year"){
        searchFieldWrapper.innerHTML = yearSearchField;
    }
}