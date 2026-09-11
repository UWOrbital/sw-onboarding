import background from "../assets/earth_compressed.webp";
import orbital_logo from "../assets/orbital_logo.png";

/**
 * @brief Background component displaying the Earth image
 * @return tsx element of Background component
 */
function Background() {
  return (
    <>
      <div className="fixed inset-0 -z-30 bg-gray-950" />
      <img
        src={background}
        alt="background-image"
        className="fixed inset-0 h-full w-full object-cover -z-20 transition-opacity duration-300 opacity-60"
      />
      <div
        className="fixed inset-0 -z-10 duration-300 bg-gradient-to-b from-gray-950/90 via-gray-950/70 to-gray-950/40"
      />
      <div className="relative z-10 flex items-center gap-3 p-4">
        <img src={orbital_logo} alt="orbital logo" className="h-10 w-auto" />
        <span className="text-white text-lg font-medium">Software Onboarding</span>
      </div>
    </>
  );
}

export default Background;
