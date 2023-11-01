import { styled } from "@mui/material";
import { LinkBox } from "components/footer/LinkBox";
const SocialBox = styled(LinkBox) `
  flex-direction: row;
  :before {
    position: absolute;
    content: "";
    width: 90%;
    height: 1px;
    background: ${props => props.theme.palette.primary[props.theme.palette.mode === "dark" ? "light" : "dark"]};
    left: 50%;
    transform: translateX(-50%);
  }
` as typeof LinkBox;

export { SocialBox };