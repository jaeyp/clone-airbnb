module.exports = {
  theme: {
    /* replacing exist styles here */

    /* extending exist styles here */
    extend: {
      spacing: {
        // "name of the class": "CSS parameter"
        "25vh": "25vh",
        "30vh": "30vh",
        "40vh": "40vh",
        "50vh": "50vh",
        "60vh": "60vh",
        "70vh": "70vh",
        "75vh": "75vh"
      },
      borderRadius: {
        xl: "1.5rem"
      },
      borderWidth: {
        "16": "16px"
      },
      backgroundSize: {
        zoom: "120%" // bg-zoom
      }
    }
  },
  variants: {
    // https://tailwindcss.com/docs/background-size#customizing
    // apply bg-zoom with hover event.
    // e.g. class="hover:bg-zoom"
    backgroundSize: ["responsive", "hover"]
  },
  plugins: []
};
