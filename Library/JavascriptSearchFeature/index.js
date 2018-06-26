// Establish variables and references to html
var $tbody = document.querySelector("tbody");
var $dateInput=document.querySelector("#date");
var $stateInput = document.querySelector("#state");
var $cityInput=document.querySelector("#city");
var $countryInput=document.querySelector("#country");
var $shapeInput=document.querySelector("#shape");

// Establish variables for search buttons
var $searchBtn = document.querySelector("#search");
var $filtersearchBtn=document.querySelector("#filtersearch");

// Add an event listener to the each search button and tie to functions below
$searchBtn.addEventListener("click", handleSearchButtonClick);
$filtersearchBtn.addEventListener("click",handleFilterSearchButtonClick);

// Initializes filtered data as all siting data
var filterdata = sitingdata;

// displayTable shows the siting data based on what filter data input
function displayTable() {
  $tbody.innerHTML = "";
  for (var r = 0; r < filterdata.length; r++) {
    // Get get the current siting object and its fields
    var siting = filterdata[r];
    var fields = Object.keys(siting);
    // Insert a new row
    var $row = $tbody.insertRow(r);
    for (var c = 0; c < fields.length; c++) {
      // Create a new cell for each siting field
      var field = fields[c];
      var $cell = $row.insertCell(c);
      $cell.innerText = siting[field];
    }
  }
}

// handleFilterSearchButtonClick allows for several combinations of user input
// Date Only, Country Only, Country+State Only, Shape Only, All Fields, No Fields
// This is done in thinking of how a user may want to filter through data without writing unnecessary code

function handleFilterSearchButtonClick() {
   
  var filterDate = $dateInput.value;
  var filterCountry = $countryInput.value.trim().toLowerCase();
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCity = $cityInput.value.trim().toLowerCase();
  var filterShape = $shapeInput.value.trim().toLowerCase();

  // If user doesn't provide any input, this will return entire siting table without filtering
  if (filterDate == "" && filterCountry == "" && filterState == "" && filterCity == "" && filterShape == "") {
    filterdata=sitingdata;
  }

  // If user provides date only, this will execute the filter on the date
  else if (filterCountry == "" && filterState == "" && filterCity == "" && filterShape == "") {filterdata=sitingdata.filter(function(siting) {
    var sitingDate=siting.datetime;
    return (sitingDate === filterDate);
  })
  }

  // If user provides country only, this will execute the filter
  else if (filterDate == "" && filterState == "" && filterCity == "" && filterShape == "") {filterdata=sitingdata.filter(function(siting) {
    var sitingCountry=siting.country;
    return (sitingCountry===filterCountry);
  })
  }
// If user provides country + state only, this will execute filter
  else if (filterDate == "" && filterCity == "" && filterShape == "") {filterdata=sitingdata.filter(function(siting) {
    var sitingCountry=siting.country;
    var sitingState=siting.state;
    return (sitingCountry===filterCountry && sitingState===filterState);
  })
  }

  // If user provides shape only, this will execute filter
  else if (filterDate == "" && filterCountry == "" && filterState == "" && filterCity == "") {filterdata=sitingdata.filter(function(siting) {
    var sitingShape=siting.shape;
    return (sitingShape===filterShape);
  })
  }
  
  else { filterdata = sitingdata.filter(function(siting) {
    var sitingDate = siting.datetime; 
    var sitingCountry=siting.country;
    var sitingState = siting.state;   
    var sitingCity=siting.city;
    var sitingShape=siting.shape;
    
    return (sitingDate===filterDate && sitingCountry===filterCountry && sitingState===filterState && sitingCity===filterCity && sitingShape===filterShape);
  });

  }
  displayTable();
}

function handleSearchButtonClick() {
  displayTable();
}





