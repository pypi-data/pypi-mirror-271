import { fuzzy_finder_callback_lookup } from "./fuzzy_finder.js";
var current_shape;
var current_view;
var rows;
var columns;
var plots_list;

var plots_div;
var colorscheme_template;

function getNumViews(){
	return Math.ceil(plots_list.length / (current_shape[0] * current_shape[1]))
}

function initAllData() {
	// const gridContainer = document.getElementById('grid-container');
	// gridContainer.innerHTML = "";
	// gridContainer.style.gridTemplateColumns = `repeat(${columns}, ${100 / columns}%)`;
	// gridContainer.style.gridTemplateRows = `repeat(${rows}, ${100 / rows}%)`;
	plots_div = [];
	for (let i = 0; i < plots_list.length; i++){
		var gridItem = document.createElement('div');
		gridItem.classList.add('grid-item');
		plots_div.push(gridItem);
		var plot_json = plots_list[i];
		// gridContainer.appendChild(gridItem); //fixes the flicker issue
		Plotly.newPlot(gridItem, plot_json.data, plot_json.layout, {'responsive': true});
		gridItem._responsiveChartHandler()
		// console.log(JSON.stringify(gridItem))
		// gridContainer.removeChild(gridItem); //fixes the flicker issue
	}
}

function displayAllData() {
	const gridContainer = document.getElementById('grid-container');
	gridContainer.innerHTML = "";
	gridContainer.style.gridTemplateColumns = `repeat(${columns}, ${100 / columns}%)`;
	gridContainer.style.gridTemplateRows = `repeat(${rows}, ${100 / rows}%)`;
	// gridContainer.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
	// gridContainer.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
	
	for (let i = 0; i < rows; i++){
		for (let j = 0; j < columns; j++){
			// var gridItem = gridContainer.children[i * columns + j];
			var position = current_view * columns * rows + i * columns + j;
			if (position < plots_list.length){
				var gridItem = plots_div[position];
				gridContainer.appendChild(gridItem);
				gridItem._responsiveChartHandler()
			}
		}
	}
}

function fetchPlotData(){
	return fetch('/grid-plotter-data')
		.then(response => response.json())
		.then(data => {
			plots_list = data.plots_list.map((plots) => JSON.parse(plots));
		})}
function fetchShapeData() {
	return fetch('/current-shape-data')
		.then (response => response.json())
		.then(data => {
			current_shape = data;
			rows = current_shape[0];
			columns = current_shape[1];
		})}
function fetchViewData() {
	return fetch('/current-view-data')
		.then(response => response.json())
		.then(data => {
			current_view = data;
		})
		.catch(error => console.error('Error fetching view data:', error));
}

function addMargins() {
	for (let i = 0; i < plots_list.length; i++){
		var layout = plots_list[i].layout
		layout.margin = {'t':30,'l':25,'b':25,'r':25};
		Plotly.relayout(plots_div[i], layout);
	}
}

function initGraphs() {
	const fetchOperations = [fetchPlotData(), fetchShapeData(), fetchViewData()];
	Promise.all(fetchOperations)
		.then(initAllData)
		.then(displayAllData)
		.then(fetchColorschemeData)
		.then(addMargins)
}

function applyColorScheme() {
	var background_color = colorscheme_template.layout.paper_bgcolor
	var font_color = colorscheme_template.layout.font.color
	document.body.style.color = font_color
	document.body.style.backgroundColor = background_color
	document.body.style.borderColor = font_color

	for (let i = 0; i < plots_list.length; i++){
		var layout = plots_list[i].layout;
		layout.template = colorscheme_template;
		Plotly.relayout(plots_div[i], layout);
	}
}


function fetchColorschemeData() {
	fetch('/colorscheme-data')
		.then(response => response.json())
		.then(data => {
			colorscheme_template = data.template;
			applyColorScheme();
			})
		.catch(error => console.error('error fetching colorscheme-data:', error));
}



function updateGraphs(){
	fetchColorschemeData();
	fetchPlotData()
		.then(displayAllData);
}

function clipView(new_view){
	return Math.max(0, Math.min(getNumViews() - 1, new_view));
}

function changeView(new_view){
	current_view = clipView(new_view);
	$.ajax({
		url: '/set-current-view-data',
		type: 'POST',
		data: {query: current_view},
		success: displayAllData
	})
}

function reshapeGrid(new_grid){
	current_shape = new_grid;
	rows = current_shape[0];
	columns = current_shape[1];

	$.ajax({
		url: '/set-current-shape-data',
		type: 'POST',
		data: {query: JSON.stringify(current_shape)},
		// success: initAllData
	})
	changeView(current_view)
}

$(document).ready(function(){
	initGraphs();
	fuzzy_finder_callback_lookup.set('update graphs', updateGraphs);
	fuzzy_finder_callback_lookup.set('update colorscheme', fetchColorschemeData);
	fuzzy_finder_callback_lookup.set('change view', changeView);
	fuzzy_finder_callback_lookup.set('reshape grid', reshapeGrid);
});

$(document).on('keydown', function(e){
	var new_view = current_view;
	if (e.keyCode === 39){ // right arrow
		e.preventDefault();
		new_view++;
	} else if (e.keyCode == 37){ // left arrow
		e.preventDefault();
		new_view--;
	} 
	else if (!$('#results').is(':visible') 
		&& e.keyCode >= 48 
		&& e.keyCode <= 57){ // between 0 and 9
		e.preventDefault();
		new_view = (e.keyCode - 48).toString();
	}
	new_view = clipView(new_view);
	if (new_view != current_view){
		changeView(new_view)
	}
});

