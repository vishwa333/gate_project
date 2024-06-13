
// Function to populate chapters dropdown based on subject
function populateChapters(chapterSelect, chapters) {
    $.each(chapters, function (index, chapter) {
        chapterSelect.append($('<option>', {
            value: chapter.value,
            text: chapter.label
        }));
    });
}

// Data for chapters based on subjects
var mathChapters = [
    { value: "chapter1", label: "Chapter 1" },
    { value: "chapter2", label: "Chapter 2" },
    { value: "chapter3", label: "Chapter 3" }
]; 

var physicsChapters = [
        { value: "chapter4", label: "Chapter 4" },
        { value: "chapter5", label: "Chapter 5" },
        { value: "chapter6", label: "Chapter 6" }
    ];

var chemistryChapters = [
        { value: "chapter7", label: "Chapter 7" },
        { value: "chapter8", label: "Chapter 8" },
        { value: "chapter9", label: "Chapter 9" }
    ];
// Function to display test data in table
function displayTestData(data, title) {
    var tableBody = $("#test-data");
    var tableTitle = $("#table-title");
    // Update table title
    tableTitle.text(title);
    // Clear existing table data
    tableBody.empty();
    // Loop through test data and create table rows
    $.each(data, function (index, item) {
        var row = $("<tr>").append(
            $("<td>").text(item.topic),
            $("<td>").text(item.questions),
            $("<td>").text(item.maxMarks),
            $("<td>").html('<button class="take-test-btn">Take Test</button>')
        );
        tableBody.append(row);
    });
}

// Populate chapters dropdown based on selected subject
$(document).on("click", "#subject", function() {
    var subject = $(this).val();
    var chapterSelect = $("#chapter");
    // Clear existing chapters
    chapterSelect.empty();
    // Populate chapters based on selected subject
    var chapters;
    switch (subject) {
        case "math":
            chapters = mathChapters;
            break;
        case "physics":
            chapters = physicsChapters;
            break;
        case "chemistry":
            chapters = chemistryChapters;
            break;
    }
    populateChapters(chapterSelect, chapters);
});

function topic_wise_test() {
    console.log("Clicked Submit");
    var subject = $("#subject").val();
    var chapter = $("#chapter").val();
    console.log(subject,chapter);
    // Simulate fetching test data based on selected subject and chapter
    var testData = [
      { topic: "Topic 1", questions: 10, maxMarks: 20 },
      { topic: "Topic 2", questions: 15, maxMarks: 30 },
      { topic: "Topic 3", questions: 20, maxMarks: 40 }
    ];
    var title = `${subject.toUpperCase()} - ${chapter}`;
    displayTestData(testData, title);
  }

// Handle form submission
$(document).on("click", "#submit-btn",topic_wise_test);


$(document).ready(function() {
    // Populate chapters dropdown on page load
    populateChapters($("#chapter"), mathChapters);
    console.log("Yes reaching in topic_wise.js");
  });
  