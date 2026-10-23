import { loadFont } from "@remotion/fonts";
import { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Audio,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const fontFamily = "Noto Sans Telugu";
// Served from public/fonts (npm @fontsource) so rendering does not depend on fonts.gstatic.com
const fontsReady = Promise.all(
  ["400", "700", "800"].map((weight) =>
    loadFont({
      family: fontFamily,
      url: staticFile(`fonts/noto-sans-telugu-telugu-${weight}-normal.woff2`),
      weight,
    }),
  ),
);

export type DayScript = {
  day: number;
  fps: number;
  durationSeconds: number;
  voiceover: string;
  hook: string;
  cards: string[];
  cta: string;
  follow: string;
};

const HOOK_SECONDS = 4;
const CTA_SECONDS = 5;

const Background: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(circle at 25% 20%, rgba(124,58,237,0.55), transparent 55%), radial-gradient(circle at 80% 80%, rgba(6,182,212,0.45), transparent 55%), #0A0A14",
    }}
  />
);

const Glass: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({
  children,
  style,
}) => (
  <div
    style={{
      background: "rgba(255,255,255,0.06)",
      backdropFilter: "blur(20px)",
      border: "1px solid rgba(255,255,255,0.1)",
      borderRadius: 24,
      padding: "48px 56px",
      ...style,
    }}
  >
    {children}
  </div>
);

const Logo: React.FC = () => (
  <div
    style={{
      position: "absolute",
      bottom: 90,
      width: "100%",
      textAlign: "center",
      color: "rgba(255,255,255,0.8)",
      fontSize: 36,
      fontWeight: 700,
      fontFamily,
    }}
  >
    Prompt Techies
  </div>
);

const Hook: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");
  const zoom = spring({ frame, fps, config: { damping: 12 }, from: 1.25, to: 1 });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 80 }}>
      <div
        style={{
          transform: `scale(${zoom})`,
          color: "#fff",
          fontSize: 84,
          fontWeight: 800,
          lineHeight: 1.3,
          textAlign: "center",
          fontFamily,
        }}
      >
        {words.map((word, i) => {
          const start = i * 4;
          const opacity = interpolate(frame, [start, start + 6], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <span key={i} style={{ opacity, marginRight: 16, display: "inline-block" }}>
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Card: React.FC<{ text: string; localFrame: number }> = ({ text, localFrame }) => {
  const { fps } = useVideoConfig();
  const enter = spring({ frame: localFrame, fps, config: { damping: 200 } });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 80 }}>
      <Glass
        style={{
          opacity: enter,
          transform: `translateY(${(1 - enter) * 60}px)`,
          color: "#fff",
          fontSize: 60,
          fontWeight: 700,
          lineHeight: 1.4,
          textAlign: "center",
          fontFamily,
        }}
      >
        {text}
      </Glass>
    </AbsoluteFill>
  );
};

const Cta: React.FC<{ text: string; follow: string }> = ({ text, follow }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 15 } });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 80 }}>
      <Glass style={{ transform: `scale(${enter})`, textAlign: "center", fontFamily }}>
        <div style={{ color: "#fff", fontSize: 56, fontWeight: 700, lineHeight: 1.4 }}>{text}</div>
        <div style={{ color: "#06B6D4", fontSize: 48, fontWeight: 800, marginTop: 40 }}>{follow}</div>
      </Glass>
    </AbsoluteFill>
  );
};

export const DayVideo: React.FC<{ script: DayScript }> = ({ script }) => {
  const [handle] = useState(() => delayRender("Loading Telugu font"));
  useEffect(() => {
    fontsReady.then(() => continueRender(handle));
  }, [handle]);

  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hookEnd = HOOK_SECONDS * fps;
  const ctaStart = (script.durationSeconds - CTA_SECONDS) * fps;
  const bodyFrames = ctaStart - hookEnd;
  const cardFrames = bodyFrames / script.cards.length;

  let body: React.ReactNode = null;
  if (frame >= hookEnd && frame < ctaStart) {
    const index = Math.min(Math.floor((frame - hookEnd) / cardFrames), script.cards.length - 1);
    const localFrame = frame - hookEnd - index * cardFrames;
    body = <Card key={index} text={script.cards[index]} localFrame={localFrame} />;
  }

  return (
    <AbsoluteFill>
      <Background />
      <Audio src={staticFile(script.voiceover)} />
      {frame < hookEnd && <Hook text={script.hook} />}
      {body}
      {frame >= ctaStart && <Cta text={script.cta} follow={script.follow} />}
      <Logo />
    </AbsoluteFill>
  );
};
