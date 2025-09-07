// Batch unfollow script for X (Twitter)
// Clicks real <button> elements with data-testid containing 'unfollow'
// How to use: Open Twitter Following Page, Load how many account that you want to unfollow, past the code in browser console (CMD + Option + I), then paste this code.

let delay = 1500; // ms between unfollows

// Grab all unfollow buttons
let buttons = Array.from(document.querySelectorAll("button[data-testid*='unfollow']"));

console.log("Found", buttons.length, "accounts to unfollow");

let count = 0;
function unfollowNext() {
    if (count >= buttons.length) {
        console.log("✅ Done unfollowing", count, "accounts");
        return;
    }

    let btn = buttons[count];
    btn.click();
    console.log("⏳ Unfollowed", count + 1, "of", buttons.length);

    // Confirm popup "Unfollow"
    setTimeout(() => {
        let confirm = Array.from(document.querySelectorAll("span"))
            .find(el => el.innerText.trim() === "Unfollow");
        if (confirm) confirm.closest("button").click();
    }, 500);

    count++;
    setTimeout(unfollowNext, delay);
}

unfollowNext();