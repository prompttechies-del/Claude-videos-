import { Composition } from "remotion";
import { DayVideo, DayScript } from "./DayVideo";
import day01 from "../../videos/day-01/script.json";

export const RemotionRoot: React.FC = () => {
  const script = day01 as DayScript;
  return (
    <Composition
      id="Day01"
      component={DayVideo}
      durationInFrames={script.durationSeconds * script.fps}
      fps={script.fps}
      width={1080}
      height={1920}
      defaultProps={{ script }}
    />
  );
};
