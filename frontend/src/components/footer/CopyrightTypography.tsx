import {styled, Typography} from "@mui/material";

const CopyrightTypography = styled(Typography) `
  text-transform: uppercase;
  letter-spacing: ${props => props.theme.spacing(0.25)};
  white-space: nowrap;
` as typeof Typography;

export { CopyrightTypography };