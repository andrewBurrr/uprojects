import React from "react";
import { CopyrightBox } from "components/footer/CopyrightBox";
import { CopyrightTypography } from "components/footer/CopyrightTypography";
import { CopyrightLink } from "components/footer/CopyrightLink";

const Copyright = () => {
    return (
        <CopyrightBox>
            <CopyrightTypography
                variant="subtitle2"
                align="center"
            >
                <CopyrightLink
                    color="inherit"
                    href="http://uprojects.ca"
                >
                    {`Copyright © uprojects.ca ${ new Date().getFullYear()}`}
                </CopyrightLink>{' '}
            </CopyrightTypography>
        </CopyrightBox>
    );
}

export { Copyright };