import { styled, Box } from "@mui/material";

const CopyrightBox = styled(Box) `
  background-color: ${props => props.theme.palette.primary['main']};
  padding-top: ${props => props.theme.spacing(1)};
  padding-bottom: ${props => props.theme.spacing(1)};
  padding-left: ${props => props.theme.spacing(2)};
  padding-right: ${props => props.theme.spacing(2)};
` as typeof Box;

export { CopyrightBox };