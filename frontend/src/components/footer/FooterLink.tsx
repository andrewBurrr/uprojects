import { styled, Link as MuiLink } from "@mui/material";

const FooterLink = styled(MuiLink) `
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: ${props => props.theme.spacing(2)};
  margin-left: ${props => props.theme.spacing(2)};
  margin-top: ${props => props.theme.spacing(1)};
  margin-bottom: ${props => props.theme.spacing(1)};
  transition: color 0.3s;
  &:hover {
    color: ${props => props.theme.palette.secondary["light"]};
  }
` as typeof MuiLink;

export { FooterLink };