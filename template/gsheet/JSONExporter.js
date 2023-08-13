const COLUMNS = ['Column 1', 'Column 2', 'Column 3'];
const IGNORE_SHEETS = [];
const LINK_LABEL = 'Example Shortcut';
const LINK_HREF = 'https://grounded-architecture.io/data';

function onOpen() {
    let ss = SpreadsheetApp.getActiveSpreadsheet();
    let menuEntries = [
        {name: 'Export Data as JSON', functionName: 'exportDataAsJSON'}
    ];
    ss.addMenu('Export Data', menuEntries);
}

function exportDataAsJSON() {
    const sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
    const sheetsData = new Array();

    for (let i = 0; i < sheets.length; i++) {
        const sheetName = sheets[i].getName();
        if (ignoreSheet(sheetName)) continue;
        sheetsData.push(extractDataFromSheet(sheetName));
    }

    const containerObject = {
        metadata: {exportDate: Utilities.formatDate(new Date(), 'GMT', 'yyyy-MM-dd')},
        data: sheetsData
    };

    displayText(JSON.stringify(containerObject, null, 2));
}


function extractDataFromSheet(sheetName) {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(sheetName);
    if (sheet == null) {
        return [];
    }

    return getRowsData(sheet, sheetName);
}


function getRowsData(sheet, source) {
    let startingRow = 1;
    let headersRange = sheet.getRange(startingRow, 1, 1, sheet.getMaxColumns());
    let headers = headersRange.getValues()[0];
    let dataRange = sheet.getRange(startingRow + 1, 1, sheet.getMaxRows(), sheet.getMaxColumns());
    let objects = getObjects(dataRange.getValues(), headers);

    return {
        source,
        data: objects
    };
}

function getObjects(data, keys) {
    const objects = [];
    const columns = COLUMNS.map(c => c.toLowerCase());

    for (let i = 0; i < data.length; ++i) {
        let object = {};
        let hasData = false;
        for (let j = 0; j < data[i].length; ++j) {
            const cellData = data[i][j];
            const key = ('' + keys[j]).toLowerCase();
            if (isCellEmpty(cellData) || key === '' || columns.indexOf(key) < 0) {
                continue;
            }
            object[('' + keys[j]).toLowerCase().replace(/ /g, '_')] = (cellData + '').replace(/"/g, '\\"');
            hasData = true;
        }
        if (hasData) {
            objects.push(object);
        }
    }
    return objects;
}

function isCellEmpty(cellData) {
    return typeof (cellData) == 'string' && cellData == '';
}

function isAlnum(char) {
    return char >= 'A' && char <= 'Z' ||
        char >= 'a' && char <= 'z' ||
        isDigit(char);
}

function isDigit(char) {
    return char >= '0' && char <= '9';
}


function displayText(text) {
    const app = HtmlService.createHtmlOutput().setTitle('Exported JSON');

    app.append('<p style="font-family: Helvetica">Shortcuts: ');
    if (LINK_LABEL && LINK_LABEL.trim().length > 0) {
        app.append('<a href="' + LINK_HREF + '" target="_blank">' + LINK_LABEL + '</a>.');
        app.append('</p>');
    }
    app.append('<textarea cols="56" rows="14">');
    app.append(htmlEscape(text));
    app.append('</textarea>');

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    ss.show(app);

    return app;
}

function htmlEscape(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function ignoreSheet(sheetName) {
    return sheetName.startsWith('_') || IGNORE_SHEETS.map(s => s.toLowerCase()).includes(sheetName.toLowerCase());
}


