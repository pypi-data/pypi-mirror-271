// document.addEventListener('DOMContentLoaded', function () {
//     const button = document.querySelector('.md-clipboard.md-icon');
//     if (!button) {
//         console.error('Button not found!');
//         return;
//     }
//
//     button.addEventListener('click', function (event) {
//         event.preventDefault();  // Prevent the default copy action
//
//         // Get the target element specified in the data-clipboard-target attribute
//         const targetSelector = button.getAttribute('data-clipboard-target');
//         const targetElement = document.querySelector(targetSelector);
//         if (!targetElement) {
//             console.error('Target element for copying not found!');
//             return;
//         }
//
//         // Get the text and modify it to remove specific patterns
//         let content = targetElement.textContent;
//         content = content.replace(/^\s*In \[\d+\]:/gm, ''); // Remove In [n]:
//         content = content.replace(/^\s*\.{3}:/gm, ''); // Remove ...:
//         content = content.replace(/^\s*\n/gm, ''); // Clean up new lines
//
//         // Remove everything after Out[n]:
//         let cleanedContent = '';
//         const lines = content.split('\n');
//
//         // const leading_space = lines[0].startsWith(' ')
//
//         for (let line of lines) {
//             if (/^\s*Out\[\d+\]:/.test(line)) break; // Stop copying if Out[n]: is found
//
//             // if (line.startsWith(' ')) {
//             //     line = line.substring(1);
//             // }
//
//             cleanedContent += line + '\n';
//         }
//         //
//         // // Use the Clipboard API to write text
//         // navigator.clipboard.writeText(cleanedContent.trim())
//         //     .then(() => {
//         //         // Notify the user that the content has been cleaned and copied
//         //         alert('Content successfully cleaned and copied to clipboard saf !');
//         //     })
//         //     .catch(err => {
//         //         console.error('Failed to copy text: ', err);
//         //     });
//     });
// });

// ------------------------------------------------------------------------


// document.addEventListener('DOMContentLoaded', function() {
//     const button = document.querySelector('.md-clipboard.md-icon');
//     if (!button) {
//         console.error('Button not found!');
//         return;
//     }
//
//     button.addEventListener('click', function(event) {
//         event.preventDefault();  // Prevent the default copy action
//
//         // Get the target element specified in the data-clipboard-target attribute
//         const targetSelector = button.getAttribute('data-clipboard-target');
//         const targetElement = document.querySelector(targetSelector);
//         if (!targetElement) {
//             console.error('Target element for copying not found!');
//             return;
//         }
//
//         // Get the text and modify it to remove specific patterns and trim one leading space
//         let content = targetElement.textContent;
//         let cleanedContent = '';
//
//         // Split content into lines and process each line individually
//         const lines = content.split('\n');
//         for (let line of lines) {
//             // Remove In [n]: and Out[n]: with all following content
//             if (/^\s*Out\[\d+\]:/.test(line)) break; // Stop copying if Out[n]: is found
//             line = line.replace(/^\s*In \[\d+\]:\s|^\s*\.{3}:\s/g, ''); // Remove In [n]: and continuation ...
//
//             //
//             // // Remove only the first leading space if it exists
//             // if (line.startsWith(' ')) {
//             //     line = line.substring(1);
//             // }
//
//             cleanedContent += line + '\n'; // Add processed line to cleaned content
//         }
//
//         // Use the Clipboard API to write text
//         // navigator.clipboard.writeText(cleanedContent.trim())
//         //     .then(() => {
//         //         // Notify the user that the content has been cleaned and copied
//         //         alert('Content successfully cleaned and copied to clipboard saf !');
//         //     })
//         //     .catch(err => {
//         //         console.error('Failed to copy text: ', err);
//         //     });
//
//         // Use the Clipboard API to write text
//         navigator.clipboard.writeText(cleanedContent.trim())
//             .catch(err => {
//                 console.error('Failed to copy text: ', err);
//             });
//     });
// });


// ------------------------------------------------------------------------


// document.addEventListener('DOMContentLoaded', function () {
//     const buttons = document.querySelectorAll('.md-clipboard.md-icon'); // Select all buttons
//     if (buttons.length === 0) {
//         console.error('No buttons found!');
//         return;
//     }
//
//     buttons.forEach(button => { // Loop through each button
//         button.addEventListener('click', function (event) {
//             event.preventDefault();  // Prevent the default copy action
//
//             // Get the target element specified in the data-clipboard-target attribute
//             const targetSelector = button.getAttribute('data-clipboard-target');
//             const targetElement = document.querySelector(targetSelector);
//             if (!targetElement) {
//                 console.error('Target element for copying not found!');
//                 return;
//             }
//
//             // Get the text and modify it to remove specific patterns and trim one leading space
//             let content = targetElement.textContent;
//             let cleanedContent = '';
//
//             // Split content into lines and process each line individually
//             const lines = content.split('\n');
//             for (let line of lines) {
//                 if (/^\s*Out\[\d+\]:/.test(line)) break; // Stop copying if Out[n]: is found
//                 line = line.replace(/^\s*In \[\d+\]:\s|^\s*\.{3}:\s/g, ''); // Remove In [n]: and continuation ...
//
//                 cleanedContent += line + '\n'; // Add processed line to cleaned content
//             }
//
//             // Use the Clipboard API to write text
//             navigator.clipboard.writeText(cleanedContent.trim())
//                 .catch(err => {
//                     console.error('Failed to copy text: ', err);
//                 });
//         });
//     });
// });

// ------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.md-clipboard.md-icon'); // Select all buttons
    if (buttons.length === 0) {
        console.error('No buttons found!');
        return;
    }

    buttons.forEach(button => { // Loop through each button
        button.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent the default copy action

            // Get the target element specified in the data-clipboard-target attribute
            const targetSelector = button.getAttribute('data-clipboard-target');
            const targetElement = document.querySelector(targetSelector);
            if (!targetElement) {
                console.error('Target element for copying not found!');
                return;
            }

            let content = targetElement.textContent;
            let cleanedContent = '';
            let copying = false;  // State variable to keep track of whether we are currently copying

            // Split content into lines and process each line individually
            const lines = content.split('\n');
            for (let line of lines) {
                if (/^\s*In \[\d+\]:/.test(line)) {
                    copying = true; // Start copying if In [n]: is found
                } else if (/^\s*Out\[\d+\]:/.test(line)) {
                    copying = false; // Stop copying if Out[n]: is found
                    cleanedContent += '\n'; // Add processed line to cleaned content
                }

                if (copying) {
                    line = line.replace(/^\s*In \[\d+\]:\s|^\s*\.{3}:\s/g, ''); // Clean In [n]: if we're copying
                    cleanedContent += line + '\n'; // Add processed line to cleaned content
                }
            }

            // Trim the final content to remove unnecessary whitespace
            cleanedContent = cleanedContent.trim();
            // Remove the final In [n]: block, if it exists, as no more lines follow it
            cleanedContent = cleanedContent.replace(/\s*In \[\d+\]:\s*$/, '').trim();

            // Use the Clipboard API to write text
            navigator.clipboard.writeText(cleanedContent)
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        });
    });
});

