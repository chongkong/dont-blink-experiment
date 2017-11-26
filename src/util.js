export default {
    PUNCTUATIONS: [".", ",", "?", "!", ";", '"', "'", "_"],

    cleanText(text) {
        return text.replace(/_(\s)/g, "$1")
    },

    magicSplit(text) {
        let words = text.split(/\s+/).reverse();
        let frames = [];
        let pop = () => words.pop().replace(/_$/, "");
        let peek = () => words[words.length - 1];
        let punctuated = w => this.PUNCTUATIONS.some(p => w.endsWith(p));
        while (words.length >= 2) {
            let frame = [pop(), pop()];
            frames.push(frame);
            if (punctuated(frame[1]))
                continue;
            if (words.length > 0)
                frame.push(pop());
            if (words.length > 0 && punctuated(peek()))
                frame.push(pop());
        }
        if (words.length > 0)
            frames.push(words.reverse());
        return frames;
    },

    waitForMillis(millis) {
        return new Promise(resolve => setTimeout(resolve, millis));
    }
}
