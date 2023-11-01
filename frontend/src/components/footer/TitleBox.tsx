import { styled, Box } from "@mui/material";

const TitleBox = styled(Box) `
  padding-top: ${props => props.theme.spacing(2)};
  padding-bottom: ${props => props.theme.spacing(2)};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
` as typeof Box;

export { TitleBox };