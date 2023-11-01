import { styled, Typography } from "@mui/material";

const TitleTypography = styled(Typography) `
  font-family: Garamond, serif;
  font-style: normal;
  letter-spacing: ${props => props.theme.spacing(0.25)};
  white-space: nowrap;
` as typeof Typography;

export { TitleTypography };