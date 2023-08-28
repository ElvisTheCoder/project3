// 1.) Use the D3 library to read in samples.json from the URL.
let url = "http://127.0.0.1:5000/LoadHousingData";

// Fetch data from url.
d3.json(url).then(function(data) {
  console.log(data);
    // let data = [ {location: 'Austin', coordinates: [], 
    // housing: ,
    // years:  , 
    // 'housing percent change': , 
    // 'median income': [50000.0, 51500.0, 53000.0, 54500.0, 56000.0, 57500.0, 59000.0, 60500.0, 62000.0, 63500.0, 65000.0, 66500.0, 68000.0, 69500.0, 71000.0, 72500.0, 74000.0, 75500.0, 77000.0, 78500.0, 80000.0, 81500.0, 83000.0],
    // 'median income percent change': [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]},

    // {location: 'San Francisco', coordinates: [], 
    // housing: [500000, 510000, 520000, 530000, 540000, 550000, 560000, 570000, 580000, 590000, 600000, 610000, 620000, 630000, 640000, 650000, 660000, 670000, 680000, 690000, 700000, 710000, 720000], 
    // years : [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]    ,
    // 'housing percent change': [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03], 
    // 'median income': [100000.0, 103000.0, 106000.0, 109000.0, 112000.0, 115000.0, 118000.0, 121000.0, 124000.0, 127000.0, 130000.0, 133000.0, 136000.0, 139000.0, 142000.0, 145000.0, 148000.0, 151000.0, 154000.0, 157000.0, 160000.0, 163000.0, 166000.0],
    // 'median income percent change': [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]
    // }];
    // console.log(data);
    // The url will give a JSON object with three keys: 
    // Austin will be shown initially.
    let transformedData = [];

// Iterate through the JSON data
for (let i = 0; i < data.length; i++) {
  let entry = data[i];
  let location = entry.location;

  // Find if this location already exists in the transformedData
  let foundLocation = transformedData.find((item) => item.location === location);

  if (foundLocation) {
    // Add to the existing location's arrays
    foundLocation.years.push(entry.years);
    foundLocation.housing.push(entry.housing);
    foundLocation["housing percent change"].push(entry["housing percent change"]);
  } else {
    // Create a new entry for this location
    transformedData.push({
      "location": location,
      "years": [entry.years],
      "housing": [entry.housing],
      "housing percent change": [entry["housing percent change"]]
    });
  }
}

console.log(transformedData);

    function init() {
      let austin_data = data.find(d => d["location"] == "Austin");
      // Housing and Income vs time
      let trace_housing = {
        type: 'line',
        x: austin_data["years"],
        y: austin_data["housing"],
        name: "Housing Cost",
        text: "", // Desription 
      };
      let trace_income = {
        type: 'line',
        x: austin_data["years"],
        y: austin_data["median income"],
        name: "Median Income  ",
        text: "", // Desription 
      };
    
      let layout1 = {
        title: "Housing vs Income in Austin"
      };
      Plotly.newPlot("bar", [trace_housing, trace_income], layout1);

      // Housing, M2, and Interest Rates vs. Time.
      let trace_housing_change = {
        type: 'line',
        x: austin_data["years"],
        y: austin_data["housing percent change"],
        name: "Housing Change Cost",
        text: "", // Desription 
      };
      
      let trace_interest = {
        type: 'line',
        x: austin_data["years"],
        y: austin_data["housing"],
        name: "Interest Rates",
        text: "", // Desription 
      };
      let trace_m2 = {
        type: 'line',
        x: austin_data["years"],
        y: austin_data["median income percent change"],
        name: "M2",
        text: "", // Desription 
      };
    
      let layout2 = {
        title: "Housing vs Interest Rates vs M2"
      };
    
      Plotly.newPlot("line", [trace_housing_change, trace_interest], layout2);


    }
    


    
    init();
    // Add onto the dropdown menu


 
      



  d3.select("#selDataset").on("change", function() {
      getData();
    });
    
  // Graph
  function getData() {
      let dropdown = d3.select("#selDataset");
      let dataset = dropdown.property("value");
      // Assuming 'data_list' is accessible and structured with the required data
      let selectedData = data.find(d => d["location"] == dataset);
      // Explain the line above: Answer: 
      // Housing and Income vs time.
      let trace_housing = {
        type: 'line',
        x: selectedData["years"],
        y: selectedData["housing"],
        name: "Housing Cost",
        text: "", // Desription 
      };
      let trace_income = {
        type: 'line',
        x: selectedData["years"],
        y: selectedData["median income"],
        name: "Median Income  ",
        text: "", // Desription 
      };
    
      let layout1 = {
        title: "Housing vs Income"
      };
      Plotly.newPlot("bar", [trace_housing, trace_income], layout1);

      // Housing, M2, and Interest Rates vs. Time.
      let trace_housing_change = {
        type: 'line',
        x: selectedData["years"],
        y: selectedData["housing"],
        name: "Housing Cost",
        text: "", // Desription 
      };
      
      let trace_interest = {
        type: 'line',
        x: selectedData["years"],
        y: selectedData["housing"],
        name: "Interest Rates",
        text: "", // Desription 
      };
      let trace_m2 = {
        type: 'line',
        x: selectedData["years"],
        y: selectedData["median income"],
        name: "M2",
        text: "", // Desription 
      };
    
      let layout2 = {
        title: "Housing vs Interest Rates vs M2"
      };
    
      Plotly.newPlot("bar", [trace_housing_change, trace_interest], layout2);

    }
  
  });

