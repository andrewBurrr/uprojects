import { styled, Box } from "@mui/material";

const LinkBox = styled(Box) `
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-right: ${props => props.theme.spacing(3)};
  padding-left: ${props => props.theme.spacing(3)};
  @media (min-width: 900px) {
    flex-direction: row;
  }
` as typeof Box;

export { LinkBox };